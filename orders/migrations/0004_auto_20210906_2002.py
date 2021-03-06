# Generated by Django 3.2.6 on 2021-09-06 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210903_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.orderitemstatus'),
        ),
    ]
