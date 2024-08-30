# Generated by Django 4.2 on 2024-08-26 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_productoffer_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasificacionpadre',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clasificacion/'),
        ),
        migrations.CreateModel(
            name='ClasificacionNieta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('padre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nietos', to='products.clasificacionhija')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='clasificaciones_nieta',
            field=models.ManyToManyField(blank=True, related_name='productos_nietos', to='products.clasificacionnieta'),
        ),
    ]