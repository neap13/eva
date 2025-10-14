from django.contrib import admin
from .models import (Especialidad, Paciente, Medico, ConsultaMedica,
                     Tratamiento, Medicamento, RecetaMedica, Aseguradora)
admin.site.register([Especialidad, Paciente, Medico, ConsultaMedica,
                     Tratamiento, Medicamento, RecetaMedica, Aseguradora])
