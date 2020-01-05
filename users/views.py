from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users.forms import UsuarioModelForm, UserModelForm, LoginModelForm
from django.http import HttpResponse
from produtos.models import Produto, Notificacao
from produtos.views import addNotificacao
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.decorators import login_required
from datetime import datetime


def cadastrar(request):
    form = UserModelForm(request.POST or None)
    usuario_form = UsuarioModelForm(request.POST or None)
    context = {'form': form, 'usuario_form': usuario_form}
    if request.method == 'POST':

        user_exists = User.objects.filter(
            username=request.POST['username']).exists()
        if not user_exists:
            if form.is_valid():
                if usuario_form.is_valid():
                    usuario = usuario_form.save(commit=False)
                    user = form.save(commit=False)
                    user.save()
                    usuario.user = user
                    usuario.save()
                    messages.success(request, "Usuário criado com sucesso!")
                    return redirect('http://127.0.0.1:8000/login')
                else:
                    messages.error(request, "usuario_form invalido")
            else:
                messages.error(request, "form invalido")
        else:
            messages.error(request, "Usuário já existente")
    return render(request, 'cadastro.html', context)


def entrar(request):
    form = LoginModelForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        try:
            user_aux = User.objects.get(username=request.POST['username'])
            usuario = authenticate(username=user_aux.username,
                                   password=request.POST["password"])
            if usuario is not None:
                login(request, usuario)
                usuario = Usuario.objects.get(user=request.user)

                # Teste notificação
                #produtos = Produto.objects.all().filter(user=request.user)
                #for p in produtos:
                #    addNotificacao(p)
                #notif = Notificacao.objects.all().filter(user=request.user)

                context = {'user': user_aux, 'usuario': usuario}
                return redirect('/painel/detalhes')
            else:
                messages.error(request, "Usuário ou senha inválidos")
        except User.DoesNotExist:
            messages.error(request, "Usuário ou senha inválidos")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário ou senha inválidos")
    return render(request, 'login.html', context)


def sair(request):
    logout(request)
    return redirect('/')


@login_required
def painel(request):

    produtos = Produto.objects.all().filter(user=request.user)
    usuario = Usuario.objects.get(user=request.user)

    context = {'produtos': produtos, 'usuario': usuario}

    if request.method == 'POST':
        form_data = request.POST.dict()
        last_name = form_data.get("last_name")
        first_name = form_data.get("first_name")
        email = form_data.get("email")
        telefone = form_data.get("telefone")
        data_nascimento = form_data.get("data_nascimento")
        tempo_notificacao = form_data.get("tempo_notificacao")

        request.user.first_name = first_name
        request.user.last_name = last_name
        usuario.email = email
        usuario.telefone = telefone
        usuario.data_nascimento = datetime.strptime(
            data_nascimento, "%Y-%m-%d").date()
        usuario.tempo_notificacao = tempo_notificacao

        request.user.save()
        usuario.save()

        messages.success(request, "Alterações salvas com sucesso!")

    return render(request, 'usuario.html', context)

@login_required
def painelProdutos(request):

    produtos = Produto.objects.all().filter(user=request.user)
    usuario = Usuario.objects.get(user=request.user)

    context = {'produtos': produtos, 'usuario': usuario}

    return render(request, 'usuario_produto.html', context)




