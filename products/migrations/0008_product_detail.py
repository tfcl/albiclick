# Generated by Django 3.1.1 on 2021-10-03 22:10

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]