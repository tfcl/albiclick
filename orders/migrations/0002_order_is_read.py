# Generated by Django 3.1.1 on 2021-10-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
