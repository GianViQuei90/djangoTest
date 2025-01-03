from django import forms
from .models import AsistenciaModel, ClienteModel, AsistenciaEmpleadoModel, EmpleadoModel, VentasModel, DetalleVentaModel, Productos
from unfold.widgets import UnfoldAdminTextInputWidget

class AsistenciaForm(forms.ModelForm):
    dni = forms.CharField(
        label="DNI del cliente", 
        max_length=20, 
        required=True,
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Ingrese DNI del cliente"})
    )

    class Meta:
        model = AsistenciaModel
        fields = []  # No mostramos los campos del modelo en el formulario directamente

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        try:
            cliente = ClienteModel.objects.get(clienteDni=dni)
        except ClienteModel.DoesNotExist:
            raise forms.ValidationError("No existe un cliente con este DNI.")
        return cliente

    def save(self, commit=True):
        cliente = self.cleaned_data['dni']
        asistencia = super().save(commit=False)
        asistencia.clienteId = cliente
        if commit:
            asistencia.save()
        return asistencia

class AsistenciaEmpleadoForm(forms.ModelForm):
    dni = forms.CharField(
        label="DNI del empleado", 
        max_length=20, 
        required=True,
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Ingrese DNI del empleado"})    
    )

    class Meta:
        model = AsistenciaEmpleadoModel
        fields = []  # No mostramos los campos del modelo en el formulario directamente

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        try:
            empleado = EmpleadoModel.objects.get(empleadoDni=dni)
        except ClienteModel.DoesNotExist:
            raise forms.ValidationError("No existe un empleado con este DNI.")
        return empleado

    def save(self, commit=True):
        empleado = self.cleaned_data['dni']
        asistencia = super().save(commit=False)
        asistencia.empleadoId = empleado
        if commit:
            asistencia.save()
        return asistencia

class VentaClienteForm(forms.ModelForm):
    dni = forms.CharField(
        label="N° DNI o RUC del cliente", 
        max_length=20, 
        required=True,
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Ingrese DNI o RUC del cliente"})
    )

    class Meta:
        model = VentasModel
        fields = []  # No mostramos directamente los campos del modelo de ventas, los manejaremos en el formulario.

    def clean_dni(self):
        """Validar si el cliente existe con el DNI ingresado."""
        dni = self.cleaned_data.get('dni')
        try:
            cliente = ClienteModel.objects.get(clienteDni=dni)
        except ClienteModel.DoesNotExist:
            raise forms.ValidationError("No existe un cliente con este DNI.")
        return cliente

    def save(self, commit=True):
        """Guardar la venta con el cliente y los detalles."""
        cliente = self.cleaned_data['dni']
        venta = super().save(commit=False)
        venta.clienteId = cliente  # Asignar el cliente basado en el DNI

        if commit:
            venta.save()

        return venta


