from django import forms
from .models import (
    Especialidad, Aseguradora, Paciente, Medico,
    Medicamento, Tratamiento, ConsultaMedica, RecetaMedica
)

class EspecialidadForm(forms.ModelForm):
    class Meta: model = Especialidad; fields = ["nombre"]

class AseguradoraForm(forms.ModelForm):
    class Meta: model = Aseguradora; fields = ["nombre", "plan"]

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["rut","nombres","apellidos","sexo","fecha_nacimiento","telefono","email","aseguradora"]

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["rut","nombres","apellidos","especialidad","registro_colegio","email","telefono"]

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ["nombre","via_administracion","indicaciones_generales"]

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ["paciente","medico","tipo","descripcion","fecha_inicio","fecha_fin","activo"]

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = ["paciente","medico","especialidad","fecha","motivo","diagnostico","precio"]

class RecetaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = ["consulta","medicamento","dosis","frecuencia","duracion_dias","indicaciones"]

# Formulario para el botón “Agenda ¡aquí!”
class ReservaRapidaForm(forms.Form):
    rut = forms.CharField(max_length=12, label="RUT")
    nombres = forms.CharField(max_length=120)
    apellidos = forms.CharField(max_length=120)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=30, label="Teléfono")
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())
    fecha = forms.DateTimeField(
        label="Fecha y hora",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    motivo = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
