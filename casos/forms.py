from django import forms
from .models import Caso

class CasoForm(forms.ModelForm):

    class Meta:
        model = Caso
        exclude = ['estatus']
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date'
            })
        }

class CambiarEstatusForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['estatus']