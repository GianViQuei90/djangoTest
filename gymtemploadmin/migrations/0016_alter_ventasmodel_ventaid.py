# Generated by Django 5.1.4 on 2024-12-29 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtemploadmin', '0015_alter_detalleventamodel_detalleid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventasmodel',
            name='ventaId',
            field=models.AutoField(db_column='venta_id', primary_key=True, serialize=False, unique=True, verbose_name='ID Venta'),
        ),
    ]
