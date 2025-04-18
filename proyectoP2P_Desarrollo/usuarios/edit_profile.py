from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['fecha_nacimiento', 'direccion', 'ingresos', 'egresos']  # Ajusta los campos que quieres permitir editar
