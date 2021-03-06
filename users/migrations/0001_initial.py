# Generated by Django 3.2.6 on 2021-09-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('gender', models.CharField(max_length=8)),
                ('email', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=128)),
                ('birthday', models.DateField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
