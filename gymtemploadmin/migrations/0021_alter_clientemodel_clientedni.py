# Generated by Django 5.1.4 on 2024-12-30 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtemploadmin', '0020_alter_clientemodel_clientetipoidentificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientemodel',
            name='clienteDni',
            field=models.CharField(db_column='cliente_dni', max_length=15, unique=True, verbose_name='N° DNI/RUC'),
        ),
    ]
