# Generated by Django 2.2.4 on 2019-11-16 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0011_produto_tempo_notificacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicopreco',
            name='preco',
            field=models.TextField(),
        ),
    ]
