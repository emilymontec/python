from django import forms
from .models import Incidente, Proyecto

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['proyecto', 'que_paso', 'gravedad', 'estado', 'creado_por', 'como_se_arreglo']
        widgets = {
            'que_paso': forms.Textarea(attrs={'rows':3}),
            'como_se_arreglo': forms.Textarea(attrs={'rows':3}),
        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':3}),
        }

class IncidenteCompleteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['como_se_arreglo', 'cerrado_por']
        widgets = {
            'como_se_arreglo': forms.Textarea(attrs={'rows':3}),
        }
