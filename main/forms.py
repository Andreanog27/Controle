from django import forms
from .models import Despesa
from .models import Receita
from .models import Categoria
from django.contrib.auth.models import User

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ["descricao", "valor", "categoria", "data", "classificacao"]
        labels = {
            "descricao": "Descrição da despesa",
            "valor": "Valor (R$)",
            "categoria": "Categoria",
            "data": "Data da despesa",
            "classificacao": "Tipo de Classificação",
        }
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'categoria', 'data']
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
 

class RegistroForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        return p2        
        
       
