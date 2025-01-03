import csv
from django.http import HttpResponse
import requests
from .models import ComprobanteModel
from django.utils.html import format_html

def export_as_csv(modeladmin, request, queryset):
    # Crear el objeto HttpResponse con un tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_export.csv"'

    # Crear un escritor CSV
    writer = csv.writer(response)
    # Escribir la fila de encabezados
    writer.writerow(['ID', 'Cliente DNI', 'Fecha de Asistencia', 'Hora de Entrada'])

    # Escribir los datos de las filas
    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.clienteId.clienteDni,  # Suponiendo que tienes un cliente relacionado
            obj.asistenciaFecha,
            obj.asistenciaHoraEntrada,
        ])

    return response

# Personaliza el nombre de la acción para que se vea en el administrador
export_as_csv.short_description = "Exportar como CSV"

def generar_comprobante(modeladmin, request, queryset):
    """
    Acción para generar un comprobante para la última venta seleccionada.
    """
    for venta in queryset.order_by('-ventaFecha')[:1]:  # Tomar la última venta
        # Generar el payload
        payload = venta.generar_payload()
        print(payload)
        # Enviar a la API
        url = "https://api.nubefact.com/api/v1/4702623e-dc9c-47b1-bd5d-763ee76ce747"
        headers = {
        'Authorization': '6adca5c4f270425eb126ef74353a3b75a157bb98b6cf4dcf8f48f6868743964b',
        'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            # Obtener el URL del comprobante y actualizar la venta
            data = response.json()
            # venta = VentasModel.objects.get(ventaId=venta_id)
            # print(data['enlace_del_pdf'])
            venta.ventaPdf = data.get("enlace_del_pdf", "")
            venta.save(update_fields=["ventaPdf",])
            url = venta.ventaPdf
            # print(url)
            # print(venta.ventaId)
            # Mensaje de éxito
            if url:

                ComprobanteModel.objects.update_or_create(
                    ventaId=venta,
                    defaults={
                        'enlace_pdf': url
                        }
                )
                # Mensaje de éxito con enlace al comprobante
                modeladmin.message_user(
                    request,
                    format_html(f'Comprobante generado: <a href="{url}" target="_blank">Ver comprobante</a>')
                )
            else:
                modeladmin.message_user(
                    request,
                    "Comprobante generado, pero no se recibió un enlace PDF.",
                    level='warning'
                )
            # modeladmin.message_user(request, format_html(f'Comprobante generado: <a href="{url}" target="_blank">Ver comprobante</a>'))
            # format_html(f'<a href="{obj.ventaPdf}" target="_blank">Ver comprobante</a>')
        except requests.exceptions.RequestException as e:
            modeladmin.message_user(request, f"Error al generar comprobante: {e}", level='error')
