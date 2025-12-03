from django.shortcuts import render, redirect, get_object_or_404
import json
import csv
import calendar
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Despesa, Categoria
from .forms import DespesaForm
from .models import Receita
from .forms import ReceitaForm
from django.contrib import messages
from django.db.models.functions import TruncMonth
from decimal import Decimal
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.db.models.functions import ExtractMonth
from .models import Despesa, Categoria


@login_required
def index(request):
    despesas = Despesa.objects.filter(usuario=request.user).order_by('-data')
    categorias = Categoria.objects.all()

    mes = request.GET.get('mes')
    ano = request.GET.get('ano')
    categoria = request.GET.get('categoria')

    if mes:
        despesas = despesas.filter(data__month=mes)
    if ano:
        despesas = despesas.filter(data__year=ano)
    if categoria:
        despesas = despesas.filter(categoria_id=categoria)

    total = despesas.aggregate(Sum("valor"))["valor__sum"] or 0

    return render(request, "index.html", {
        "despesas": despesas,
        "total": total,
        "categorias": categorias,
    })

@login_required
def adicionar_despesa(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            return redirect('index')
    else:
        form = DespesaForm()

    return render(request, "adicionar.html", {"form": form})

def nova_despesa(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        categoria_id = request.POST['categoria']  # agora recebemos um ID

        categoria = get_object_or_404(Categoria, id=categoria_id)
        

        Despesa.objects.create(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            data=datetime.today(),
            usuario=request.user
        )

        return redirect('dashboard')

    return render(request, 'nova_despesa.html', {'categorias': categorias})

@login_required
def adicionar_receita(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            return redirect('index')
    else:
        form = DespesaForm()

    return render(request, "adicionar_receita.html", {"form": form})

@login_required
def listar_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'receitas.html', {'receitas': receitas})

@login_required
def excluir_receita(request, receita_id):
    if request.method == "POST":
        try:
            receita = Receita.objects.get(id=receita_id, usuario=request.user)
        except Receita.DoesNotExist:
            messages.error(request, "Receita não encontrada ou não pertence a você.")
            return redirect("listar_receitas")

        receita.delete()
        messages.success(request, "Receita excluída com sucesso!")
        return redirect("listar_receitas")

    messages.warning(request, "A exclusão deve ser feita via POST.")
    return redirect("listar_receitas")


def relatorios(request):
    categorias = Categoria.objects.all()
    despesas = Despesa.objects.filter(usuario=request.user)

    # Pegando filtros da URL (GET)
    categoria_id = request.GET.get("categoria")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Aplicando filtros
    if categoria_id and categoria_id.isdigit():
        despesas = despesas.filter(categoria_id=categoria_id)
    
    if data_inicio:
        despesas = despesas.filter(data__gte=data_inicio)
    
    if data_fim:
        despesas = despesas.filter(data__lte=data_fim)

    return render(request, "relatorios.html", {
        "categorias": categorias,
        "despesas": despesas,
        "filtro_categoria": int(categoria_id) if categoria_id else None,
        "filtro_data_inicio": data_inicio,
        "filtro_data_fim": data_fim,
    })
     

def registrar(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # loga automaticamente
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    usuario = request.user
    despesas = Despesa.objects.filter(usuario=usuario).order_by("data")

    # Total gasto
    total_gastos = despesas.aggregate(total=Sum("valor"))["total"] or 0

    # Média mensal
    media_mensal = total_gastos / 12 if total_gastos > 0 else 0

    # Gráfico mensal
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    valores_gastos = []
    for mes in range(1, 12 + 1):
        total_mes = despesas.filter(data__month=mes).aggregate(total=Sum("valor"))["total"]
        valores_gastos.append(float(total_mes) if total_mes else 0)

    # Gráfico de pizza (categorias do banco)
    categorias_labels = list(Categoria.objects.values_list("nome", flat=True))

    categorias_valores = []
    for nome in categorias_labels:
        total_cat = despesas.filter(categoria__nome=nome).aggregate(total=Sum("valor"))["total"]
        categorias_valores.append(float(total_cat) if total_cat else 0)

    context = {
        "despesas": despesas,
        "total_gastos": total_gastos,
        "media_mensal": media_mensal,
        "meses": meses,
        "valores_gastos": valores_gastos,
        "categorias_labels": categorias_labels,
        "categorias_valores": categorias_valores,
    }

    return render(request, "dashboard.html", context)

@login_required
def excluir_despesa(request, despesa_id):
    """
    Exclui uma despesa do usuário logado de forma segura.
    - Se a despesa não existir ou não pertencer ao usuário, mostra mensagem de erro.
    - Se excluída com sucesso, mostra mensagem de sucesso.
    """
    if request.method == 'POST':
        try:
            despesa = Despesa.objects.get(id=despesa_id, usuario=request.user)
        except Despesa.DoesNotExist:
            messages.error(request, "Despesa não encontrada ou não pertence a você.")
            return redirect('dashboard')

        despesa.delete()
        messages.success(request, f"Despesa '{despesa.descricao}' excluída com sucesso!")
        return redirect('dashboard')

    # Se acessar via GET, apenas redireciona
    messages.warning(request, "A exclusão deve ser feita via botão de confirmação.")
    return redirect('dashboard')

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, "Categoria excluída com sucesso!")
    return redirect('index')

@login_required
def exportar_excel(request):
    despesas = Despesa.objects.filter(usuario=request.user).order_by("-data")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Despesas"

    # Cabeçalho
    colunas = ["Descrição", "Valor", "Categoria", "Data"]
    ws.append(colunas)

    # Dados
    for despesa in despesas:
        ws.append([
            despesa.descricao,
            float(despesa.valor),
            despesa.categoria.nome if despesa.categoria else "",
            despesa.data.strftime("%d/%m/%Y")
        ])

    # Ajusta largura das colunas
    for col in ws.columns:
        max_len = 0
        col_letra = get_column_letter(col[0].column)

        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))

        ws.column_dimensions[col_letra].width = max_len + 2

    # Resposta HTTP com o arquivo
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=despesas.xlsx"
    wb.save(response)

    return response

def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="despesas.csv"'

    writer = csv.writer(response)
    writer.writerow(["Descrição", "Categoria", "Valor", "Data"])

    despesas = Despesa.objects.all()
    for d in despesas:
        writer.writerow([d.descricao, d.categoria, d.valor, d.data])

    return response
