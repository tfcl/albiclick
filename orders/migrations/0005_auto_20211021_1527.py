# Generated by Django 3.1.1 on 2021-10-21 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20211011_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=120)),
                ('is_free_shipping', models.BooleanField()),
                ('discount', models.IntegerField()),
                ('max_redeem', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='cupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.cupon'),
        ),
    ]