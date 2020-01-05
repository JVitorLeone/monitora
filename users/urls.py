from django.urls import path
from . import views as user_views
from produtos import views as prod_views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('detalhes/', user_views.painel, name="painel"),
    path('produto/ajax/delete_prod/', prod_views.deleteProd, name="deleteProd"),
    path('produto/', user_views.painelProdutos, name="painel_produtos"),
    path('<int:id_produto>', prod_views.detalheProduto, name="detalhe_prod"),
    path('ajax/delete_prod/', prod_views.deleteProd, name='deleteProd'),
]