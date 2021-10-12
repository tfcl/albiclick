# Generated by Django 3.1.1 on 2021-10-11 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.payment'),
        ),
    ]