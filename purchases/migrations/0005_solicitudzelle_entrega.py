# Generated by Django 4.1.13 on 2024-08-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_solicitudzelleitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudzelle',
            name='entrega',
            field=models.CharField(choices=[('pending', 'En espera'), ('accepted', 'Entregada'), ('canceled', 'Cancelada')], default='pending', max_length=10),
        ),
    ]
