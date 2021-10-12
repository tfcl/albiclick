# Generated by Django 3.1.1 on 2021-09-10 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '__first__'),
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('note', models.CharField(max_length=120)),
                ('state', models.CharField(choices=[('1', 'A Aguardar Pagamento'), ('2', 'Pagamento Confirmado'), ('3', 'Em Processamento'), ('4', 'Enviado')], max_length=1)),
                ('invoice', models.FileField(null=True, upload_to='uploads/')),
                ('tracking_number', models.CharField(max_length=120, null=True)),
                ('creation_date', models.DateField(auto_now=True)),
                ('payment_receipt', models.FileField(null=True, upload_to='uploads/')),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_adress', to='users.adress')),
                ('adress_billing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_adress_billing', to='users.adress')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cart')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.payment')),
                ('shipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.shipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=120)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.payment')),
            ],
        ),
    ]