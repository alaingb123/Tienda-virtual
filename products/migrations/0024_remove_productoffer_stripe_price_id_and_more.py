# Generated by Django 4.2 on 2024-08-25 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_productoffer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoffer',
            name='stripe_price_id',
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='products.product', unique=True),
        ),
    ]