# Generated by Django 4.1.13 on 2024-07-22 14:39

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Alain\\Downloads\\PortableGit\\micro-ecommerce\\local-cdn\\protected'), upload_to=products.models.handle_product_attachment_upload),
        ),
    ]
