# Generated by Django 2.1.2 on 2018-10-29 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=12)),
                ('nombre', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
