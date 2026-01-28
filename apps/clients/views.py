from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Client
from .forms import ClientForm

# Mixin personalizado para verificar si es encargador
class EncargadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Encargador').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a clientes')
        return redirect('home')

# Lista de clientes (solo encargadores)
class ClientListView(LoginRequiredMixin, EncargadorRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'client_list'

# Ver detalles de un cliente (solo encargadores)
class ClientDetailView(LoginRequiredMixin, EncargadorRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

# Crear nuevo cliente (solo encargadores)
class ClientCreateView(LoginRequiredMixin, EncargadorRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado correctamente')
        return super().form_valid(form)

# Editar cliente existente (solo encargadores)
class ClientUpdateView(LoginRequiredMixin, EncargadorRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado correctamente')
        return super().form_valid(form)

# Eliminar cliente (solo encargadores)
class ClientDeleteView(LoginRequiredMixin, EncargadorRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente eliminado correctamente')
        return super().delete(request, *args, **kwargs)