from rest_framework import serializers
from .models import (
    Especialidad, Aseguradora, Paciente, Medico,
    Medicamento, Tratamiento, ConsultaMedica, RecetaMedica
)

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta: model = Especialidad; fields = '__all__'

class AseguradoraSerializer(serializers.ModelSerializer):
    class Meta: model = Aseguradora; fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    aseguradora_nombre = serializers.CharField(source='aseguradora.nombre', read_only=True)
    sexo_display = serializers.CharField(source='get_sexo_display', read_only=True)
    class Meta: model = Paciente; fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    class Meta: model = Medico; fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    via_administracion_display = serializers.CharField(source='get_via_administracion_display', read_only=True)
    class Meta: model = Medicamento; fields = '__all__'

class TratamientoSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='paciente.nombres', read_only=True)
    medico_nombre = serializers.CharField(source='medico.nombres', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    class Meta: model = Tratamiento; fields = '__all__'
    def validate(self, attrs):
        fi = attrs.get('fecha_inicio') or getattr(self.instance, 'fecha_inicio', None)
        ff = attrs.get('fecha_fin') or getattr(self.instance, 'fecha_fin', None)
        if fi and ff and ff < fi:
            raise serializers.ValidationError("La fecha de término no puede ser menor a la de inicio.")
        return attrs

class ConsultaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='paciente.nombres', read_only=True)
    medico_nombre   = serializers.CharField(source='medico.nombres', read_only=True)
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    class Meta: model = ConsultaMedica; fields = '__all__'
    def validate_precio(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

class RecetaSerializer(serializers.ModelSerializer):
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True)
    class Meta: model = RecetaMedica; fields = '__all__'
