from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from datetime import date, timedelta
from django.core.validators import MinValueValidator
from datetime import datetime
import json
# Create your models here.

class ClienteModel(models.Model):

    GENERO=(
        ('masculino', 'Masculino'), 
        ('femenino', 'Femenino')
    )
    TIPO=(
        ('ruc', 'RUC'), 
        ('dni', 'DNI')
    )
    clienteId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'cliente_id',
        verbose_name='ID'
    )
    clienteTipoIdentificacion = models.CharField(
        choices=TIPO,
        max_length=15,
        null= False,
        db_column='cliente_tipo_identificacion',
        verbose_name='DNI/RUC',
        default= 'dni'
    )
    clienteDni = models.CharField(
        max_length=15,
        null= False,
        unique = True,
        db_column='cliente_dni',
        verbose_name='N° DNI/RUC'
    )
    clienteNombre = models.CharField(
        max_length=100,
        null= False,
        db_column='cliente_nombre',
        verbose_name='Nombre'
    )
    clienteApellido = models.CharField(
        max_length=100,
        null= False,
        db_column='cliente_apellido',
        verbose_name='Apellido'
    )
    clienteGenero = models.CharField(
        max_length=50,
        choices=GENERO,
        db_column='cliente_genero',
        default='masculino',
        verbose_name='Genero'
    )
    clienteFechaNacimiento = models.DateField(
        null= False,
        db_column='cliente_fecha_nacimiento',
        verbose_name='Fecha de nacimiento'
    )
    clienteCelular = models.CharField(
        max_length=15,
        null= False,
        db_column='cliente_celular',
        verbose_name='Celular'
    )
    clienteCorreo = models.EmailField(
        db_column='cliente_correo',
        max_length=30,
        verbose_name='Correo',
        unique=True
    )
    clienteFechaRegistro = models.DateTimeField(
        auto_now_add=True,
        db_column='cliente_fecha_registro',
        verbose_name='Fecha de registro'
    )
    clienteDireccion = models.CharField(
        db_column='cliente_direccion',
        max_length=150,
        verbose_name='Direccion',
        unique=False,
        default= 'calle A S/N, San Martin de Porres'
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        db_table = 't_cliente'
        verbose_name = 'cliente'
        verbose_name_plural='clientes'

class AsistenciaModel(models.Model):
    clienteId = models.ForeignKey(
        to=ClienteModel, 
        on_delete=models.CASCADE,
        related_name='asistencias',
        db_column='cliente_id',
        verbose_name='ID'
    )
    asistenciaFecha = models.DateField(
        auto_now_add=True,
        db_column='cliente_asistencia',
        verbose_name='Fecha de asistencia'
    )
    asistenciaHoraEntrada = models.TimeField(
        auto_now_add=True,
        db_column='cliente_hora_entrada',
        verbose_name='Hora de entrada'
    )
    class Meta:
        db_table = 't_asistencia'
        verbose_name = 'asistencia'
        verbose_name_plural='asistencias clientes'

    def __str__(self):
        return f'de {self.clienteId.clienteNombre}'
    
class MembresiaModel(models.Model):
    TIPOS_MEMBRESIA = (
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    )

    clienteId = models.ForeignKey(
        to=ClienteModel, 
        on_delete=models.CASCADE,
        related_name='membresias',
        db_column='cliente_id',
        verbose_name='ID'
    )
    membresiaTipo = models.CharField(
        max_length=50,
        db_column='membresia_tipo',
        choices=TIPOS_MEMBRESIA,
        verbose_name="Tipo"
    )  # Ej: Mensual, Trimestral
    membresiaPrecio = models.DecimalField(
        max_digits=10, 
        db_column='membresia_precio',
        decimal_places=2,
        verbose_name="Precio"
    )
    membresiaInicio = models.DateField(
        auto_now_add=True, 
        db_column='membresia_registro',
        verbose_name="Fecha de inicio"
    )
    membresiaDuracion = models.PositiveIntegerField(
        db_column='membresia_duracion',
        verbose_name="Duracion(días)"
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        db_table = 't_membresia'
        verbose_name = 'membresia'
        verbose_name_plural = 'membresias'

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para autocompletar la duración."""
        DURACIONES = {
            'mensual': 30,
            'trimestral': 90,
            'semestral': 180,
            'anual': 365,
        }
        if self.membresiaTipo in DURACIONES:
            self.membresiaDuracion = DURACIONES[self.membresiaTipo]  # Asigna la duración según el tipo
        super().save(*args, **kwargs)

    @property
    def dias_restantes(self):
        """Calcula los días restantes de la membresía."""
        fecha_fin = self.membresiaInicio + timedelta(days=self.membresiaDuracion)
        dias_restantes = (fecha_fin - date.today()).days
        return max(dias_restantes, 0)
    
    @property
    def esta_vencida(self):
        """Determina si la membresía ha vencido."""
        fecha_fin = self.membresiaInicio + timedelta(days=self.membresiaDuracion)
        return date.today() < fecha_fin
    
class EmpleadoModel(models.Model):
    empleadoId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'empleado_id',
        verbose_name='ID'
    )
    empleadoDni = models.CharField(
        max_length=10,
        null= False,
        unique = True,
        db_column='empleado_dni',
        verbose_name='DNI'
    )
    empleadoNombre = models.CharField(
        max_length=100,
        null= False,
        db_column='empleado_nombre',
        verbose_name='Nombre'
    )
    empleadoApellido = models.CharField(
        max_length=100,
        null= False,
        db_column='empleado_apellido',
        verbose_name='Apellido'
    )
    empleadoFechaNacimiento = models.DateField(
        null= False,
        db_column='empleado_fecha_nacimiento',
        verbose_name='Fecha de nacimiento'
    )
    empleadoCelular = models.CharField(
        max_length=15,
        null= False,
        db_column='empleado_celular',
        verbose_name='Celular'
    )
    empleadoCorreo = models.EmailField(
        db_column='empleado_correo',
        max_length=30,
        verbose_name='Correo',
        unique=True
    )
    empleadoFechaRegistro = models.DateTimeField(
        auto_now_add=True,
        db_column='empleado_fecha_registro',
        verbose_name='Fecha de registro'
    )
    empleadoFechaContratacion = models.DateTimeField(
        
        db_column='empleado_fecha_contratacion',
        verbose_name='Fecha de contratacion'
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        db_table = 't_empleado'
        verbose_name = 'empleado'
        verbose_name_plural='empleados'

class AsistenciaEmpleadoModel(models.Model):
    empleadoId = models.ForeignKey(
        to=EmpleadoModel, 
        on_delete=models.CASCADE,
        null= True,
        related_name='asistencia_empleado',
        db_column='empleado_id',
        verbose_name='ID'
    )
    asistenciaEmpleadoFecha = models.DateField(
        auto_now_add=True,
        db_column='empleado_asistencia',
        verbose_name='Fecha de asistencia'
    )
    asistenciaEmpleadoHoraEntrada = models.TimeField(
        auto_now_add=True,
        db_column='empleado_hora_entrada',
        verbose_name='Hora de entrada'
    )
    class Meta:
        db_table = 't_asistencia_empleado'
        verbose_name = 'asistencia empleado'
        verbose_name_plural='asistencias empleados'

    def __str__(self):
        return f'de {self.empleadoId.empleadoNombre}'
    
class Productos(models.Model):
    CATEGORIA=(
        ('servicio', 'Servicio'), 
        ('producto', 'Producto')
    )

    productoId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'producto_id',
        verbose_name='ID'
    )
    productoCategoria = models.CharField(
        max_length=50,
        choices=CATEGORIA,
        db_column='producto_categoria',
        default='producto',
        verbose_name='Categoria'
    )
    productoNombre = models.CharField(
        max_length=100,
        null= False,
        db_column='producto_nombre',
        verbose_name='Nombre'
    )
    productoPrecio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        db_column= 'producto_precio',
        verbose_name='Precio'
    )
    productoStock = models.PositiveIntegerField(
        default=0,
        db_column= 'producto_stock',
        verbose_name='Stock'
    )
    productoImagen = models.ImageField(
        upload_to='productos/', 
        null=True, 
        blank=True,
        db_column= 'producto_imagen',
        verbose_name='Imagen'
    )
    class Meta:
        db_table = 't_productos'
        verbose_name = 'producto'
        verbose_name_plural='productos'

    def __str__(self):
        return self.productoNombre 

class VentasModel(models.Model):
    ventaId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'venta_id',
        verbose_name='ID Venta'
    )
    clienteId = models.ForeignKey(
        to=ClienteModel, 
        on_delete=models.CASCADE,
        related_name='ventas',
        db_column='cliente_id',
        verbose_name='ID'
    )
    ventaFecha = models.DateTimeField(
        auto_now_add=True,
        db_column='venta_fecha',
        verbose_name='Fecha de venta'
    )
    ventaTotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        db_column='venta_total',
        verbose_name='Total'
    )
    ventaPdf= models.URLField(
        blank=True, 
        null=True, 
        db_column='venta_pdf',
        verbose_name="Comprobante"
    )
    class Meta:
        db_table = 't_ventas'
        verbose_name = 'venta'
        verbose_name_plural='ventas'

    def __int__(self):
        return self.ventaId

    def calcular_total(self):
        """Suma los subtotales de los detalles relacionados."""
        return sum(detalle.subtotal for detalle in self.detalles.all())

    def save(self, *args, **kwargs):
        # Calcula el total antes de guardar
        if not self.pk:
            super().save(*args, **kwargs)  # Guardar antes de calcular el total

        self.ventaTotal = self.calcular_total()
        super().save(update_fields=['ventaTotal'])

    def generar_payload(venta_id):
        try:
            # Obtener la venta y los detalles asociados
            venta = VentasModel.objects.get(ventaId=venta_id)
            detalles = DetalleVentaModel.objects.filter(ventaId=venta)
            tipo_comprobante = 2 if venta.clienteId.clienteTipoIdentificacion == "dni" else 1
            tipo_documento = 1 if venta.clienteId.clienteTipoIdentificacion == "dni" else 6
            serie = "BBB1" if venta.clienteId.clienteTipoIdentificacion == "dni" else "FFF1"
            # Crear el payload base
            payload = {
                "operacion": "generar_comprobante",
                "tipo_de_comprobante": tipo_comprobante,  # Ejemplo: Factura o Boleta, adaptar según el caso
                "serie": serie,  # Ajustar la serie según tu negocio
                "numero": str(venta.ventaId),
                "sunat_transaction": 1,
                "cliente_tipo_de_documento": tipo_documento,  # Asumiendo que este campo existe en ClienteModel
                "cliente_numero_de_documento": venta.clienteId.clienteDni,
                "cliente_denominacion": venta.clienteId.clienteNombre,  # Cambia según el nombre en tu modelo
                "cliente_direccion": venta.clienteId.clienteDireccion,  # Asegúrate de que este campo exista
                "fecha_de_emision": venta.ventaFecha.strftime("%d/%m/%Y"),
                "moneda": 1,  # 1 = Soles, adaptar según la moneda
                "porcentaje_de_igv": 18.00,
                "total_gravada": round(float(venta.ventaTotal) / 1.18, 2),  # Total sin IGV
                "total_igv": round(float(venta.ventaTotal) - float(venta.ventaTotal) / 1.18, 2),  # Solo IGV
                "total": float(venta.ventaTotal),
                "formato_de_pdf" : "TICKET",


                "items": []
            }

            # Crear los items del detalle de la venta
            for detalle in detalles:
                unidad_de_medida = "NIU" if detalle.producto.productoCategoria == "producto" else "ZZ"
                subtotal_sin_igv = (float(detalle.producto.productoPrecio) / 1.18) * detalle.cantidad
                item = {
                    "unidad_de_medida": unidad_de_medida,  # Unidad de medida estándar
                    "codigo": detalle.producto.productoId,  # ID del producto
                    "descripcion": detalle.producto.productoNombre,  # Nombre del producto
                    "cantidad": detalle.cantidad,
                    "valor_unitario": round(float(detalle.producto.productoPrecio) / 1.18, 2),  # Precio sin IGV
                    "precio_unitario": float(detalle.producto.productoPrecio),  # Precio con IGV
                    "subtotal": round(subtotal_sin_igv, 2),  # Total del ítem con IGV
                    "tipo_de_igv": 1,  # General IGV
                    "igv": round(float(detalle.subtotal) - float(detalle.subtotal) / 1.18, 2),  # Solo IGV del ítem
                    "total": float(detalle.subtotal),  # Total con IGV
                    "anticipo_regularizacion": False
                }
                payload["items"].append(item)

            # Convertir el payload a JSON
            payload_json = json.dumps(payload, indent=4)
            return payload_json

        except VentasModel.DoesNotExist:
            return "La venta especificada no existe."
        except Exception as e:
            return f"Error al generar el payload: {e}"

class DetalleVentaModel(models.Model):
    detalleId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'detalle_id',
        verbose_name='ID Detalle'
    )
    ventaId = models.ForeignKey(
        to=VentasModel, 
        on_delete=models.CASCADE,
        related_name='detalles',
        db_column='venta_id',
        verbose_name='ID Venta'
    )
    producto = models.ForeignKey(
        to = Productos,
        on_delete=models.PROTECT,
        related_name='detalles_venta',
        db_column= 'producto_detalle',
        verbose_name= 'Producto detalle'
    )
    cantidad = models.IntegerField(
        verbose_name="Cantidad",
        db_column= 'producto_cantidad',
        default=1
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        db_column= 'subtotal',
        verbose_name="Subtotal",
        blank=True, 
        default=0.00
    )
    def save(self, *args, **kwargs):
        # Calcula automáticamente el subtotal basado en el precio del producto y la cantidad
        if self.producto and self.cantidad:
            self.subtotal = self.producto.productoPrecio * self.cantidad
        super().save(*args, **kwargs)
        if self.ventaId:
            self.ventaId.ventaTotal = self.ventaId.detalles.aggregate(total=models.Sum('subtotal'))['total'] or 0.00
            self.ventaId.save()

    class Meta:
        db_table = 't_detalles'
        verbose_name = 'detalle'
        verbose_name_plural='detalles'

    # def __int__(self):
    #     return self.ventaId.ventaId
    def __str__(self):
        return f"{self.producto.productoNombre} - {self.cantidad}"
    
class ComprobanteModel(models.Model):
    comprobanteId = models.AutoField(
        primary_key= True,
        unique = True,
        db_column= 'comprobante_id',
        verbose_name='ID Comprobante'
    )
    ventaId = models.OneToOneField(
        to = VentasModel,
        on_delete= models.CASCADE,
        related_name='comprobante',
        db_column='venta_id',
        verbose_name='ID Venta'
    )
    enlace_pdf = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        db_column='comprobante_pdf',
        verbose_name="Enlace del PDF"
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Generación",
        db_column='fecha'
    )
    class Meta:
        db_table = 't_comprobantes'
        verbose_name = 'comprobante'
        verbose_name_plural='comprobantes'