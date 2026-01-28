from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# Mixin personalizado para verificar si es encargador
class EncargadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Encargador').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para realizar esta acción')
        return redirect('products:product_list')

# Lista de productos (todos los usuarios autenticados pueden ver)
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'

# Ver detalles de un producto (todos los usuarios autenticados pueden ver)
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

# Crear nuevo producto (solo encargadores)
class ProductCreateView(LoginRequiredMixin, EncargadorRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto creado correctamente')
        return super().form_valid(form)

# Editar producto existente (solo encargadores)
class ProductUpdateView(LoginRequiredMixin, EncargadorRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado correctamente')
        return super().form_valid(form)

# Eliminar producto (solo encargadores)
class ProductDeleteView(LoginRequiredMixin, EncargadorRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado correctamente')
        return super().delete(request, *args, **kwargs)