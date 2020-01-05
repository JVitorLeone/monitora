from django.urls import path
from . import views
from produtos.views import TelaCadastroProduto, TelaListaProdutos

app_name = 'produtos'

urlpatterns = [
    path('', TelaListaProdutos.as_view(), name="produtos"),
    path('cadastro/', TelaCadastroProduto.as_view(), name='cadastro_produtos'),
    path('cadastro/ajax/busca_preco/', views.buscaPreco, name='busca_preco'),
    path('ajax/adiciona_produto/', views.adicionaProduto, name='adiciona_produto'),
]