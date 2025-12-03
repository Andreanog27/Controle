from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']

        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor-input'}),
        }

