from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import exportar_excel, exportar_csv

def logout_view(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    path('', views.index, name='index'),

    # DESPESAS
    path('adicionar/', views.adicionar_despesa, name='adicionar_despesa'),
    path('despesa/nova/', views.nova_despesa, name='nova_despesa'),
    path('despesa/<int:despesa_id>/excluir/', views.excluir_despesa, name='excluir_despesa'),
   


    # RECEITAS
    path("receitas/", views.listar_receitas, name="listar_receitas"),
    path("receitas/adicionar/", views.adicionar_receita, name="adicionar_receita"),
     path('receita/excluir/<int:id>/', views.excluir_receita, name='excluir_receita'),
   

    # RELATÓRIOS & DASHBOARD
    path('relatorios/', views.relatorios, name='relatorios'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # EXPORTAÇÃO
    path("export/excel/", exportar_excel, name="exportar_excel"),
    path("export/csv/", exportar_csv, name="exportar_csv"),

    # AUTENTICAÇÃO (apenas login/logout via views do app usuarios)
    # OBS: as rotas de login/registrar ficam em usuarios.urls (incluídas no project/urls.py)
    path('login/', views.fazer_login, name='login'),   # se você usa uma view no main para login, mantenha; caso contrário, remova
    path('logout/', logout_view, name='logout'),
]
