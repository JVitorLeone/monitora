from django.shortcuts import render, redirect
from produtos.models import Produto, HistoricoPreco, Notificacao
from produtos.forms import SortProdForm, CadastroProdForm
from uuid import uuid4
from urllib.parse import urlparse
from django.core import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import pytz
import json
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.print_jobs()



def index(request):
    produtos = Produto.objects.all().order_by('data_cadastro')
    return render(request, 'indexteste.html', {'produtos': produtos})


class TelaListaProdutos(View):
    context = dict.fromkeys(['produtos_user', 'produtos', 'sort_form'])

    @csrf_exempt
    def post(self, request):
        sort_form = SortProdForm(request.POST)

        if sort_form.is_valid():
            produtos = Produto.objects.all().filter(nome=request.POST['nome'])
            self.context['produtos'] = produtos
            self.context['sort_form'] = sort_form

            return render(request, 'produtos.html', self.context)

    def get(self, request):
        self.context['sort_form'] = SortProdForm()
        try:
            self.context['produtos_user'] = Produto.objects.all().filter(user=request.user)
            self.context['produtos'] = Produto.objects.all().exclude(user=request.user).order_by('data_cadastro')
        except TypeError:
            self.context['produtos'] = Produto.objects.all().order_by('data_cadastro')
        return render(request, 'produtos.html', self.context)

@csrf_exempt
def buscaPreco(request):
    url = request.POST.get("url")

    if not url:
        messages.error(request, "URL Inválida")
        return JsonResponse({'Error': 'URL Inválida'})

    if not is_valid_url(url):
        messages.error(request, "URL Inválida")
        return JsonResponse({'Error': 'URL Inválida'})

    preco_produto = getProdutoInfos(url)

    print(preco_produto['preco'])

    if preco_produto['erro']:
        messages.error(request, preco_produto['erro'])
        return JsonResponse({'Error': preco_produto['erro']})
        
    jsonData = { 
        'url': url,
        'preco_produto': preco_produto['preco'][0],
        }

    return JsonResponse(jsonData)

        
class TelaCadastroProduto(View):

    context = dict.fromkeys(['produtos_user', 'url_form', 'sort_form', 'cadastro_form', 'produto', 'preco']) 

    @csrf_exempt
    def post(self, request):

        self.context['produtos_user'] = Produto.objects.all().filter(user=request.user)
        self.context['prod_form'] = CadastroProdForm()
        prod_form = CadastroProdForm(request.POST)

        if prod_form.is_valid:
            
            url = request.POST.get('url')

            if not url:
                messages.error(request, "URL Inválida")
                return render(request, 'cadastro_produto.html', self.context)

            if not is_valid_url(url):
                messages.error(request, "URL Inválida")
                return render(request, 'cadastro_produto.html', self.context)

            produto = Produto()
            produto.url = request.POST.get("url")
            produto.preco_atual = request.POST.get("preco_atual")
            produto.nome = request.POST.get("nome")
            produto.tempo_notificacao = request.POST.get("tempo_notificacao")

            print("other one " + str(produto.preco_atual))

            try:
                salvaProdutoBD(produto, request.user)
                hist = HistoricoPreco()
                hist.preco = produto.preco_atual
                hist.produto = produto
                hist.save()
                print("atualizou")

                # Adiciona uma tarefa agendada para o produto, 
                # que atualiza o preço do produto de acordo com o 
                # tempo definido pelo usuário
                global scheduler
                scheduler.add_job(
                    atualizaPreco, 'interval', 
                    minutes=int(produto.tempo_notificacao), 
                    args=(produto, ), 
                    id=str(produto.id_produto),
                )

                self.context['produtos_user'] = Produto.objects.all().filter(user=request.user)
                messages.success(request, "Produto cadastrado na sua lista")

                return render(request, 'cadastro_produto.html', self.context)

            except Exception as e:
                messages.error(request, e)
                return render(request, 'cadastro_produto.html', self.context)

            
    def get(self, request):

        self.context['produtos_user'] = Produto.objects.all().filter(user=request.user).order_by('data_cadastro')
        self.context['prod_form'] = CadastroProdForm()
        return render(request, 'cadastro_produto.html', self.context)


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


def getProdutoInfos(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    result = requests.get(url, headers=headers)
    data_set = dict(url=url, nome=[], preco=[], descricao=[], erro=[])
    
    if result:
        print("Procurando preço...")
        produto_infos = {
            # "nome": ['name', 'nome', 'title'],
            "preco": ['price', 'preco', 'valor', 'value', 'Valor'],
            # "descricao": ['description', 'descricao', 'about'],
        }

        tags = ['meta', 'span', 'strong', 'h1', 'h2', 'h3', 'p']
        properties = ['itemprop', 'name', 'content', 'class', 'id']

        soup = BeautifulSoup(result.text, "html.parser")

        for key, values in produto_infos.items():
            for tag in tags:
                for prop in properties:
                    for value in values:
                        if (soup.find_all(tag, attrs={prop: re.compile(value)})):
                            for data in soup.find_all(tag, attrs={prop: re.compile(value)}):
                                if data.find_all(text=True):
                                    text = data.get_text()
                                    print(text)
                                else:
                                    text = data.get('content')
                                    print(text)

                                if text is not None:
                                    if isPrice(text):
                                        data_set[key].append(text)

                                   

            print(key + " ===== ")
            print(data_set[key])
            if not data_set[key]:
                data_set['erro'] = "Não conseguimos encontrar o preço do produto :/"

    else:
        data_set['erro'].append("Não conseguimos entrar em contato com a URL :/")

    return data_set

def salvaProdutoBD(produto, user):
    produto.save()
    produto.user.add(user)


def isPrice(text):
    return re.match(r"^(R\$|\$)?\s?(\d{1,3}([.,]]\d{3})*|(\d+))([.,]\d{2})?$", text)

@csrf_exempt
def adicionaProduto(request):
    user = request.user
    produto = Produto.objects.get(id_produto=request.POST['produto_id'])
    produto.user.add(user)
    json = {'success': 'Success'}
    return JsonResponse(json)

def atualizaPreco(produto):
    p = Produto.objects.get(id_produto=produto.id_produto)
    print("Atualizando produto " + str(p.id_produto))
    novo_preco = getProdutoInfos(p.url)

    p.preco_atual = novo_preco['preco'][0]
    p.save()

    hist = HistoricoPreco()
    hist.preco = novo_preco['preco'][0]
    hist.produto = p
    hist.data = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
    hist.save()

def addNotificacao(produto):
    notif = Notificacao()
    notif.produto = produto
    msg = "Novo preco: " + produto.preco_atual
    notif.mensagem = msg
    notif.save()
    print(produto.user.all())
    for user in produto.user.all():
        notif.user.add(user)
    


@csrf_exempt
def deleteProd(request):
    try:
        print(request.POST.get('id_produto'))
        produto = Produto.objects.get(id_produto=request.POST['id_produto'])
        if produto.user.count() == 1:
            global scheduler
            scheduler.remove_job(str(produto.id_produto))
            produto.delete()    
        else: 
            produto.user.remove(request.user)
        
        json = {'success': 'Produto removido!'}
            
    except Produto.DoesNotExist:
        json = {'error': "Desculpe, houve um problema"}
    except apscheduler.jobstores.base.JobLookupError:
        produto.delete() 
        json = {'success': 'Produto removido!'}

    return JsonResponse(json)

def detalheProduto(request, id_produto):
    context = {}

    if request.method == 'POST':
        produto = Produto.objects.get(id_produto = id_produto)
        produto.nome = request.POST['nome']
        produto.tempo_notificacao = request.POST['tempo_atualizacao']
        produto.save()
        try:
            job = scheduler.get_job(str(produto.id_produto))
            job.modify(minutes= int(produto.tempo_notificacao))
        except:
            pass
    try:
        produto = Produto.objects.get(id_produto = id_produto)
        historico = HistoricoPreco.objects.all().filter(produto = produto).values('data', 'preco')

        def myconverter(o):
            if isinstance(o, datetime):
                o = o - timedelta(hours=3)
                return o.strftime("%d/%m/%y %H:%M")

        historico_json = json.dumps(list(historico), default= myconverter)
        context = {'produto': produto, 'historico': historico_json}
        return render(request, 'detalhe_produto.html', context)
    except Exception as e:
        messages.error(request, e)
        return render(request, 'detalhe_produto.html', context)

def atualiza(produto):
    try:
        last_preco = str(HistoricoPreco.objects.all().filter(produto_id=produto.id_produto).last())
        produto.preco_atual = last_preco
        produto.save()
    except:
        pass

produtos = Produto.objects.all()
for produto in produtos:
    atualiza(produto)