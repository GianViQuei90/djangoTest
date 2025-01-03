from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVentaModel, Productos

@receiver(post_save, sender=DetalleVentaModel)
def actualizar_stock(sender, instance, **kwargs):
    """
    Actualiza el stock del producto cuando se registra un detalle de venta.
    """
    producto = instance.producto
    cantidad_vendida = instance.cantidad

    if producto.productoStock >= cantidad_vendida:
        producto.productoStock -= cantidad_vendida
        producto.save()
    else:
        raise ValueError(f"Stock insuficiente para el producto {producto.productoNombre}")
