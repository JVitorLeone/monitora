from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Produto(models.Model):

    objects = models.Manager()

    unique_id = models.CharField(max_length=100, null=True)
    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=512)
    descricao = models.TextField()
    url = models.TextField(blank=True)
    preco_atual = models.TextField(null=True)
    data_cadastro = models.DateTimeField(default=timezone.now, blank=True)
    tempo_notificacao = models.IntegerField(default=30, blank=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        """String for representing the Model object."""
        return self.nome
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('product-detail', args=[str(self.id_produto)])


class HistoricoPreco(models.Model):

    objects = models.Manager()

    id_historico = models.AutoField(primary_key=True)
    data = models.DateTimeField(default=timezone.now, blank=True)
    preco = models.TextField()
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """String for representing the Model object."""
        str(self.data)
        return str
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('hist-detail', args=[str(self.id_historico)])

class Notificacao(models.Model):
    objects = models.Manager()

    id_notificacao = models.AutoField(primary_key=True)
    vista = models.BooleanField(default=0)
    data = models.DateTimeField(default=timezone.now, blank=True)
    mensagem = models.TextField()
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    user = models.ManyToManyField(User)



