from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # redireciona para a home
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('usuarios:login') if False else render(request, "login.html")

    return render(request, "login.html")


def registrar(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar = request.POST.get("confirmar")

        if senha != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return redirect('usuarios:registrar')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe.")
            return redirect('usuarios:registrar')

        # cria e seta a senha corretamente
        usuario = User(username=username, email=email)
        usuario.set_password(senha)
        usuario.save()

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect('usuarios:login')

    return render(request, "registrar.html")


def sair(request):
    logout(request)
    return redirect('usuarios:login')
