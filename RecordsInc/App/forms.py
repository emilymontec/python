from django import forms
from .models import Incidente

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['proyecto', 'que_paso', 'gravedad', 'estado', 'como_se_arreglo']
        widgets = {
            'que_paso': forms.Textarea(attrs={'rows':3}),
            'como_se_arreglo': forms.Textarea(attrs={'rows':3}),
        }
