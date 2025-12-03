from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import index, adicionar_despesa, nova_despesa, dashboard, registrar, excluir_despesa, exportar_excel
from .views import exportar_csv


def logout_view(request):
    logout(request)
    return redirect('/')


urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar/', views.adicionar_despesa, name='adicionar_despesa'),
    path('despesa/nova/', views.nova_despesa, name='nova_despesa'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar/', views.registrar, name='registrar'),
    path("receitas/", views.listar_receitas, name="listar_receitas"),
    path("receitas/adicionar/", views.adicionar_receita, name="adicionar_receita"),
    path("receitas/excluir/<int:receita_id>/", views.excluir_receita, name="excluir_receita"),
    path('logout/', logout_view, name='logout'),
    path('despesa/<int:despesa_id>/excluir/', views.excluir_despesa, name='excluir_despesa'),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
    path("export/excel/", exportar_excel, name="exportar_excel"),
    path("export/csv/", exportar_csv, name="exportar_csv"),
    
    
]