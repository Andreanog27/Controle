from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

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
    
