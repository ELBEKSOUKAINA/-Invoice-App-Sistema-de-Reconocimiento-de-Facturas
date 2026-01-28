from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroForm, LoginForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Encargador').exists():
            return redirect('dashboard_encargador')
        else:
            return redirect('dashboard_cliente')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                
                if user.groups.filter(name='Encargador').exists():
                    return redirect('dashboard_encargador')
                else:
                    return redirect('dashboard_cliente')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_cliente')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            cliente_group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(cliente_group)
            
            login(request, user)
            messages.success(request, f'Cuenta creada exitosamente para {user.username}')
            return redirect('dashboard_cliente')
    else:
        form = RegistroForm()
    
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('home')

@login_required
def dashboard_cliente(request):
    if request.user.groups.filter(name='Encargador').exists():
        return redirect('dashboard_encargador')
    return render(request, 'dashboard_cliente.html', {'user': request.user})

@login_required
def dashboard_encargador(request):
    if not request.user.groups.filter(name='Encargador').exists():
        return redirect('dashboard_cliente')
    return render(request, 'dashboard_encargador.html', {'user': request.user})

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})