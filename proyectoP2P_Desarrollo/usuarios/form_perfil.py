from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['direccion', 'fecha_nacimiento', 'ingresos', 'egresos']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresos': forms.NumberInput(attrs={'class': 'form-control'}),
            'egresos': forms.NumberInput(attrs={'class': 'form-control'}),
        }
