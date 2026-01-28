from django.urls import path
from .views_auth import (
    login_view, logout_view, register_view, 
    profile_view, dashboard_cliente, dashboard_encargador
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/cliente/', dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/encargador/', dashboard_encargador, name='dashboard_encargador'),
]