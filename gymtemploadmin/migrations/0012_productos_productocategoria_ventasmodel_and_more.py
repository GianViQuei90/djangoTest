# Generated by Django 5.1.4 on 2024-12-28 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtemploadmin', '0011_alter_productos_options_alter_productos_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='productoCategoria',
            field=models.CharField(choices=[('servicio', 'Servicio'), ('producto', 'Producto')], db_column='producto_categoria', default='producto', max_length=50, verbose_name='Categoria'),
        ),
        migrations.CreateModel(
            name='VentasModel',
            fields=[
                ('ventaId', models.AutoField(db_column='venta_id', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('ventaFecha', models.DateTimeField(auto_now_add=True, db_column='venta_fecha', verbose_name='Fecha de venta')),
                ('ventaTotal', models.DecimalField(db_column='venta_total', decimal_places=2, max_digits=10, verbose_name='Total')),
                ('ventaPdf', models.URLField(blank=True, db_column='venta_pdf', null=True, verbose_name='Comprobante')),
                ('clienteId', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='gymtemploadmin.clientemodel', verbose_name='ID')),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
                'db_table': 't_ventas',
            },
        ),
        migrations.CreateModel(
            name='DetalleVentaModel',
            fields=[
                ('detalleId', models.AutoField(db_column='venta_id', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('precio_unitario', models.DecimalField(db_column='producto_precio', decimal_places=2, max_digits=10, verbose_name='Precio Unitario')),
                ('subtotal', models.DecimalField(db_column='subtotal', decimal_places=2, max_digits=10, verbose_name='Subtotal')),
                ('producto', models.ForeignKey(db_column='producto_detalle', on_delete=django.db.models.deletion.PROTECT, related_name='detalles_venta', to='gymtemploadmin.productos', verbose_name='Producto detalle')),
                ('ventaId', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='gymtemploadmin.ventasmodel', verbose_name='ID')),
            ],
        ),
    ]