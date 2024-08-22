# Generated by Django 4.2 on 2024-08-22 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0005_destinatario_instrucciones_entrega'),
        ('pedidos_stripe', '0005_alter_purchase_handle_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='destinatario',
        ),
        migrations.CreateModel(
            name='PedidoDestinatario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='extra.destinatario')),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_destinatario', to='pedidos_stripe.purchase')),
            ],
        ),
    ]
