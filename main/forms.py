from django import forms
from .models import Despesa
from .models import Receita

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ["descricao", "valor", "categoria", "data", "classificacao"]
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "classificacao": forms.Select(attrs={"class": "form-control"}),
        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ["descricao", "valor", "categoria", "data", "classificacao"]
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "classificacao": forms.Select(attrs={"class": "form-control"}),
        }
        
       
