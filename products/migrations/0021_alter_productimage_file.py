# Generated by Django 4.1.13 on 2024-08-23 15:40

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='E:\\Programs\\git-portable\\Tienda-virtual\\local-cdn\\protected'), upload_to=products.models.handle_product_attachment_upload),
        ),
    ]