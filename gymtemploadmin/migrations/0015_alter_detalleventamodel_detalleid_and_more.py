# Generated by Django 5.1.4 on 2024-12-28 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtemploadmin', '0014_alter_detalleventamodel_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventamodel',
            name='detalleId',
            field=models.AutoField(db_column='detalle_id', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='detalleventamodel',
            name='ventaId',
            field=models.ForeignKey(db_column='venta_id', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='gymtemploadmin.ventasmodel', verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ventasmodel',
            name='ventaTotal',
            field=models.DecimalField(db_column='venta_total', decimal_places=2, default=0.0, max_digits=10, verbose_name='Total'),
        ),
    ]
