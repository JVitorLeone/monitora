from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Usuario(models.Model):

    objects = models.Manager()

    id_usuario = models.AutoField(primary_key=True)
    telefone = models.CharField(max_length=32)
    data_nascimento = models.DateField()
    email = models.EmailField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def parseBirthday (self):
        birthday = self.data_nascimento.strftime('%Y-%m-%d')
        return birthday
