from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  
from django.shortcuts import redirect
from django.contrib import messages
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemFormSet
from apps.clients.models import Client
from apps.products.models import Product 

# Mixin personalizado para verificar si es encargador
class EncargadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Encargador').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para realizar esta acción')
        return redirect('invoices:invoice_list')

# Lista de facturas
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoice_list'
    
    def get_queryset(self):
        # Si es encargador, ve todas las facturas
        if self.request.user.groups.filter(name='Encargador').exists():
            return Invoice.objects.all()
        # Si es cliente, ve solo las facturas de su cliente asociado
        else:
            try:
                # Buscar el cliente asociado al usuario actual
                cliente = Client.objects.get(usuario=self.request.user)
                return Invoice.objects.filter(cliente=cliente)
            except Client.DoesNotExist:
                # Si el usuario no tiene cliente asociado, no ve facturas
                return Invoice.objects.none()

# Ver detalles de una factura
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir los items de la factura al contexto
        context['items'] = self.object.items.all()
        return context
    
    def get_queryset(self):
        # Si es encargador, puede ver cualquier factura
        if self.request.user.groups.filter(name='Encargador').exists():
            return Invoice.objects.all()
        # Si es cliente, solo puede ver facturas de su cliente
        else:
            try:
                cliente = Client.objects.get(usuario=self.request.user)
                return Invoice.objects.filter(cliente=cliente)
            except Client.DoesNotExist:
                return Invoice.objects.none()

# Crear nueva factura (CON PRODUCTOS)
class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoices:invoice_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Lista de productos para el template
        context['product_list'] = Product.objects.filter(activo=True)
        
        if self.request.POST:
            context['item_formset'] = InvoiceItemFormSet(self.request.POST)
        else:
            context['item_formset'] = InvoiceItemFormSet()
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if not self.request.user.groups.filter(name='Encargador').exists():
            try:
                cliente = Client.objects.get(usuario=self.request.user)
                form.instance.cliente = cliente
            except Client.DoesNotExist:
                messages.error(self.request, 'No tienes un cliente asociado. Contacta al encargador.')
                return redirect('invoices:invoice_list')
        
        if item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            messages.success(self.request, 'Factura creada correctamente')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Editar factura existente (solo encargadores)
class InvoiceUpdateView(LoginRequiredMixin, EncargadorRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoices:invoice_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Lista de productos para el template
        context['product_list'] = Product.objects.filter(activo=True)
        
        if self.request.POST:
            context['item_formset'] = InvoiceItemFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['item_formset'] = InvoiceItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            messages.success(self.request, 'Factura actualizada correctamente')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Eliminar factura (solo encargadores)
class InvoiceDeleteView(LoginRequiredMixin, EncargadorRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'invoices/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoices:invoice_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Factura eliminada correctamente')
        return super().delete(request, *args, **kwargs)