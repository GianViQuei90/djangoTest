# Generated by Django 5.1.4 on 2024-12-27 15:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtemploadmin', '0009_clientemodel_clientegenero'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('productoId', models.AutoField(db_column='producto_id', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('productoNombre', models.CharField(db_column='producto_nombre', max_length=100, verbose_name='Nombre')),
                ('productoPrecio', models.DecimalField(db_column='producto_precio', decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio')),
                ('productoStock', models.PositiveIntegerField(db_column='producto_stock', default=0, verbose_name='Stock')),
                ('productoImagen', models.ImageField(blank=True, db_column='producto_imagen', null=True, upload_to='productos/', verbose_name='Imagen')),
            ],
        ),
    ]
