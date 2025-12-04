from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.CharField(
        max_length=20,
        default='geral'   # coloque qualquer padrão que fizer sentido
    )

    def __str__(self):
        return self.nome



class Despesa(models.Model):
    CLASSIFICACAO_CHOICES = [
        ('fixa', 'Fixa'),
        ('variavel', 'Variável'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField()
    classificacao = models.CharField(
        max_length=10,
        choices=CLASSIFICACAO_CHOICES,
        default='variavel'
    )

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    CATEGORIAS = [
        ("renda_fixa", "Renda Fixa"),
        ("renda_variavel", "Renda Variável"),
        ("renda_extra", "Renda Extra"),
        ("outros", "Outros"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    data = models.DateField()

    def __str__(self):
        return self.descricao
    
