# Generated by Django 4.2 on 2024-08-20 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0002_destinatario'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Destinatario',
        ),
        migrations.DeleteModel(
            name='Municipio',
        ),
    ]
