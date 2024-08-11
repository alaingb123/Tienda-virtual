# Generated by Django 4.1.13 on 2024-08-09 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_clasificacion_parent'),
        ('purchases', '0007_purchase_entrega_alter_solicitudzelle_entrega'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.CreateModel(
            name='SolicitudStripeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='purchases.purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ManyToManyField(related_name='pedidos_stripe', to='products.product'),
        ),
    ]
