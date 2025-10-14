import django_filters
from .models import Medico, Paciente, ConsultaMedica, Tratamiento, Medicamento, RecetaMedica

class MedicoFilter(django_filters.FilterSet):
    especialidad = django_filters.NumberFilter(field_name='especialidad_id', lookup_expr='exact')
    class Meta: model = Medico; fields = ['especialidad']

class PacienteFilter(django_filters.FilterSet):
    rut = django_filters.CharFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(method='by_nombre')
    def by_nombre(self, qs, name, value):
        return qs.filter(nombres__icontains=value) | qs.filter(apellidos__icontains=value)
    class Meta: model = Paciente; fields = ['rut','nombre','aseguradora']

class ConsultaFilter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter()
    medico = django_filters.NumberFilter(field_name='medico_id')
    paciente = django_filters.NumberFilter(field_name='paciente_id')
    especialidad = django_filters.NumberFilter(field_name='especialidad_id')
    class Meta: model = ConsultaMedica; fields = ['medico','paciente','especialidad','fecha']

class TratamientoFilter(django_filters.FilterSet):
    tipo = django_filters.CharFilter(lookup_expr='exact')
    paciente = django_filters.NumberFilter(field_name='paciente_id')
    medico = django_filters.NumberFilter(field_name='medico_id')
    class Meta: model = Tratamiento; fields = ['tipo','paciente','medico','activo']

class MedicamentoFilter(django_filters.FilterSet):
    via_administracion = django_filters.CharFilter(lookup_expr='exact')
    class Meta: model = Medicamento; fields = ['via_administracion']

class RecetaFilter(django_filters.FilterSet):
    medicamento = django_filters.NumberFilter(field_name='medicamento_id')
    consulta = django_filters.NumberFilter(field_name='consulta_id')
    class Meta: model = RecetaMedica; fields = ['medicamento','consulta']
