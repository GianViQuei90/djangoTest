# Generated by Django 5.1.4 on 2024-12-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('clienteId', models.AutoField(db_column='cliente_id', primary_key=True, serialize=False, unique=True)),
                ('clienteDni', models.CharField(db_column='cliente_dni', max_length=10, verbose_name='DNI del cliente')),
                ('clienteNombre', models.CharField(db_column='cliente_nombre', max_length=100, verbose_name='Nombre del cliente')),
                ('clienteApellido', models.CharField(db_column='cliente_apellido', max_length=100, verbose_name='Nombre del cliente')),
                ('clienteFechaNacimiento', models.DateField(db_column='cliente_fecha_nacimiento', verbose_name='Fecha de nacimiento del cliente')),
                ('clienteCelular', models.CharField(db_column='cliente_celular', max_length=15, verbose_name='Celular del cliente')),
                ('clienteCorreo', models.EmailField(db_column='cliente_correo', max_length=30, unique=True, verbose_name='Correo del usuario')),
                ('clienteFechaRegistro', models.DateTimeField(auto_now_add=True, db_column='cliente_fecha_registro', verbose_name='Fecha de registro del personal')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'db_table': 't_cliente',
            },
        ),
    ]
