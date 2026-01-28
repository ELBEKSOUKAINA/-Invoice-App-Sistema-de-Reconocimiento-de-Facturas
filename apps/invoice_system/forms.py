from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Formulario de registro
class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label=_("Usuario"),
        max_length=150,
        help_text=_("Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_."),
        error_messages={
            'unique': _("Este usuario ya existe."),
        }
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_(
            "Tu contraseña no puede ser demasiado similar a tu información personal.<br>"
            "Tu contraseña debe contener al menos 8 caracteres.<br>"
            "Tu contraseña no puede ser una contraseña común.<br>"
            "Tu contraseña no puede ser completamente numérica."
        ),
    )
    password2 = forms.CharField(
        label=_("Confirmación de contraseña"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Introduce la misma contraseña que antes, para verificación."),
    )

    class Meta:
        model = User
        fields = ("username",)

# Formulario de login
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Usuario"),
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput,
    )