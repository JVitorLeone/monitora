# Generated by Django 2.2.4 on 2019-10-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0008_auto_20191010_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=512),
        ),
    ]
