from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import ClienteModel, AsistenciaModel, MembresiaModel, EmpleadoModel, AsistenciaEmpleadoModel, Productos, DetalleVentaModel, VentasModel, ComprobanteModel
from .forms import AsistenciaForm, AsistenciaEmpleadoForm, VentaClienteForm
from .utils import export_as_csv, generar_comprobante
from django.contrib import messages
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import TextFilter, FieldTextFilter, RangeDateFilter
# Register your models here.
# admin.site.site_header = " Gym TemploFit Admin"
# admin.site.site_title = "Mi Sitio Admin"
# admin.site.index_title = "Bienvenido al Panel de Administración"

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class MembresiaInline(TabularInline):
    model = MembresiaModel
    extra = 1  # Número de formularios adicionales en blanco que aparecerán
    fields = ('membresiaTipo', 'membresiaPrecio','is_active')  # Campos visibles
    verbose_name = "Membresia"
    verbose_name_plural = "Membresias"

class ClienteAdmin(ModelAdmin):
    list_display = ('clienteId','clienteDni','clienteNombre', 'clienteApellido', 'clienteGenero','membresia_tipo_actual', 'dias_restantes_membresia')  # Campos en la lista
    search_fields = ('clienteNombre', 'clienteApellido', 'clienteCorreo')  # Campos para búsqueda
    list_filter = ('clienteDni',)  # Filtros por fecha
    ordering = ('-clienteFechaRegistro',)
    inlines = [MembresiaInline]

    def membresia_tipo_actual(self, obj):
        """Obtiene el tipo de la membresía más reciente del cliente"""
        ultima_membresia = obj.membresias.order_by('-membresiaInicio').first()
        return ultima_membresia.membresiaTipo if ultima_membresia else "Sin membresía"
    membresia_tipo_actual.short_description = "Tipo de Membresía"

    def dias_restantes_membresia(self, obj):
        membresia = obj.membresias.filter(is_active=True).first()
        if membresia:
            return membresia.dias_restantes
        else:
            return 'sin membresia'
admin.site.register(ClienteModel, ClienteAdmin)

class AsistenciaAdmin(ModelAdmin, ImportExportModelAdmin):
    form = AsistenciaForm  # Usamos el formulario personalizado
    list_display = ('get_cliente_dni', 'asistenciaFecha', 'asistenciaHoraEntrada')  # Campos visibles en la lista
    search_fields = ('clienteId__clienteDni', 'clienteId__clienteNombre', 'clienteId__clienteApellido')  # Buscar por DNI o nombre
    list_filter_submit = True
    list_filter = ('asistenciaFecha', 'clienteId__clienteApellido')  # Filtrar asistencias por fecha
    actions = [export_as_csv]
    import_form_class = ImportForm
    export_form_class = ExportForm
    # def response_add(self, request, obj, post_url_continue=None):
    #     # Sobrescribimos response_add para evitar el mensaje automático
    #     return super().response_add(request, obj, post_url_continue=None)
    
    # def response_change(self, request, obj):
    #     # Sobrescribimos response_change para evitar el mensaje automático en cambios
    #     return super().response_change(request, obj)
    
    def save_model(self, request, obj, form, change):
        # Guardar la asistencia
        super().save_model(request, obj, form, change)

        # Obtener la membresía activa del cliente
        membresia = obj.clienteId.membresias.filter(is_active=True).first()

        if membresia:
            dias_restantes = membresia.dias_restantes
            messages.success(
                request,
                f'Asistencia registrada correctamente. La membresía del cliente vence en {dias_restantes} días.'
            )
        else:
            messages.warning(
                request,
                'Asistencia registrada correctamente, pero el cliente no tiene una membresía activa.'
            )

    def get_cliente_dni(self, obj):
        return obj.clienteId.clienteDni  # Accede al DNI del cliente relacionado

    get_cliente_dni.short_description = 'DNI'

admin.site.register(AsistenciaModel, AsistenciaAdmin)

class MembresiaAdmin(ModelAdmin):
    list_display = ('get_cliente_dni', 'membresiaTipo', 'membresiaPrecio', 'membresiaInicio', 'mostrar_dias_restantes', 'mostrar_esta_vencida')
    search_fields = ('clienteId__clienteDni', 'clienteId__clienteNombre')
    list_filter = ('membresiaTipo', 'membresiaInicio')

    def mostrar_dias_restantes(self, obj):
        return obj.dias_restantes

    mostrar_dias_restantes.short_description = "Días restantes"

    def mostrar_esta_vencida(self, obj):
        return obj.esta_vencida

    mostrar_esta_vencida.short_description = "Vencimiento"
    mostrar_esta_vencida.boolean= True

    def get_cliente_dni(self, obj):
        return obj.clienteId.clienteDni  # Accede al DNI del cliente relacionado

    get_cliente_dni.short_description = 'DNI'

admin.site.register(MembresiaModel, MembresiaAdmin)

class EmpleadoAdmin(ModelAdmin):
    list_display = ('empleadoId','empleadoDni','empleadoNombre', 'empleadoApellido', 'empleadoFechaNacimiento','empleadoFechaContratacion', 'empleadoCelular')  # Campos en la lista
    search_fields = ('empleadoDni', 'empleadoApellido', 'empleadoNombre')  # Campos para búsqueda
    list_filter = ('empleadoDni',)  # Filtros por fecha
    ordering = ('-empleadoFechaRegistro',)
    # inlines = [MembresiaInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        empleado = obj.empleadoNombre

        if empleado:
            nombre = empleado
            messages.success(
                request,
                f'El empleado: {nombre} fue creado satisfactoriamente.'
            )
        else:
            messages.warning(
                request,
                'Hubo un error al crear el empleado.'
            )


admin.site.register(EmpleadoModel, EmpleadoAdmin)

class AsistenciaEmpleadoAdmin(ModelAdmin):
    form = AsistenciaEmpleadoForm  # Usamos el formulario personalizado
    list_display = ('get_empleado_dni', 'asistenciaEmpleadoFecha', 'asistenciaEmpleadoHoraEntrada')  # Campos visibles en la lista
    search_fields = ('empleadoId__empleadoDni', 'empleadoId__empleadoNombre', 'empleadoId__empleadoApellido')  # Buscar por DNI o nombre
    list_filter = ('asistenciaEmpleadoFecha','empleadoId__empleadoApellido')  # Filtrar asistencias por fecha
    # actions = [export_as_csv]

    def get_empleado_dni(self, obj):
        if obj.empleadoId:  # Verifica si empleadoId no es None
            return obj.empleadoId.empleadoDni
        # return "Sin asignar"  # Accede al DNI del cliente relacionado

    get_empleado_dni.short_description = 'DNI'

admin.site.register(AsistenciaEmpleadoModel, AsistenciaEmpleadoAdmin)

class ProductoAdmin(ModelAdmin):
    list_display = ('productoNombre','productoCategoria', 'productoPrecio', 'productoStock', 'imagen_preview')

    def imagen_preview(self, obj):
        if obj.productoImagen:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.productoImagen.url)
        return "Sin imagen"

    imagen_preview.short_description = "Vista previa"

admin.site.register(Productos, ProductoAdmin)

class DetalleVentaInline(TabularInline):
    model = DetalleVentaModel
    extra = 1  # Cuántas filas vacías agregar inicialmente
    fields = ('producto', 'cantidad')  # Campos a mostrar en el inline # Hacemos que el subtotal sea de solo lectura

    def save_model(self, request, obj, form, change):
        # Calculamos el subtotal antes de guardar
        if obj.producto and obj.cantidad:
            obj.subtotal = obj.producto.productoPrecio * obj.cantidad
        super().save_model(request, obj, form, change)

    def subtotal(self, obj):
        return obj.subtotal  # Muestra el subtotal calculado en el inline

    subtotal.short_description = 'Subtotal'

class VentasModelAdmin(ModelAdmin):
    form = VentaClienteForm  # Usamos el formulario personalizado
    list_display = ('ventaId', 'get_dni', 'ventaFecha', 'ventaTotal')  # Campos a mostrar
    search_fields = ('clienteId__clienteDni', 'clienteId__clienteNombre')  # Buscar por DNI o nombre
    list_filter = ('clienteId__clienteDni', 'clienteId__clienteNombre')
    inlines = [DetalleVentaInline]  # Añadimos los detalles de la venta
    actions = [generar_comprobante]

    def get_dni(self, obj):
        if obj.clienteId:  # Verifica si empleadoId no es None
            return obj.clienteId.clienteDni
        # return "Sin asignar"  # Accede al DNI del cliente relacionado

    get_dni.short_description = 'N° DNI o RUC'

    # def ver_comprobante(self, obj):
    #     """
    #     Muestra un enlace al comprobante si existe.
    #     """
    #     if obj.ventaPdf:
    #         # return format_html(f'<a href="{obj.ventaPdf}" target="_blank">Ver comprobante</a>')
    #         return obj.ventaPdf
    #     return "No disponible"

    # ver_comprobante.short_description = "Comprobante"
    
    def save_model(self, request, obj, form, change):
        # Guardamos el modelo de venta
        super().save_model(request, obj, form, change)
        # Calculamos el total de la venta después de guardar los detalles
        obj.ventaTotal = obj.calcular_total()
        obj.save()

admin.site.register(VentasModel, VentasModelAdmin)

class DetallesModelAdmin(ModelAdmin):
    list_display = ('detalleId','get_venta', 'producto', 'cantidad', 'subtotal')  # Campos a mostrar
    search_fields = ('ventaId__ventaId','ventaId__clienteId__clienteDni')  # Buscar por DNI o nombre
    list_filter = ('ventaId__clienteId__clienteDni',)
    
    def get_venta(self, obj):
        if obj.ventaId:  # Verifica si empleadoId no es None
            return obj.ventaId.ventaId
        # return "Sin asignar"  # Accede al DNI del cliente relacionado

    get_venta.short_description = 'ID VENTA'

admin.site.register(DetalleVentaModel, DetallesModelAdmin)

class ComprobanteModelAdmin(ModelAdmin):
    list_display = ('comprobanteId','get_venta', 'ver_comprobante', 'fecha_generacion')
    search_fields = ('ventaId__ventaId','ventaId__clienteId__clienteDni')  # Buscar por DNI o nombre
    list_filter = ('ventaId__clienteId__clienteDni',)

    def get_venta(self, obj):
        if obj.ventaId:  # Verifica si empleadoId no es None
            return obj.ventaId.ventaId
        # return "Sin asignar"  # Accede al DNI del cliente relacionado

    get_venta.short_description = 'ID VENTA'

    def ver_comprobante(self, obj):
        """
        Muestra un enlace al comprobante si existe.
        """
        if obj.enlace_pdf:
            return format_html(f'<a href="{obj.enlace_pdf}" target="_blank">Ver comprobante</a>')
        return "No disponible"
    
    ver_comprobante.short_description = "Enlace Comprobante"

admin.site.register(ComprobanteModel, ComprobanteModelAdmin)