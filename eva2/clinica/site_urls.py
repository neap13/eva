from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('especialidades/', views.EspecialidadList.as_view(), name='especialidad_list'),
    path('especialidades/crear/', views.EspecialidadCreate.as_view(), name='especialidad_create'),
    path('especialidades/<int:pk>/editar/', views.EspecialidadUpdate.as_view(), name='especialidad_update'),
    path('especialidades/<int:pk>/eliminar/', views.EspecialidadDelete.as_view(), name='especialidad_delete'),

    path('aseguradoras/', views.AseguradoraList.as_view(), name='aseguradora_list'),
    path('aseguradoras/crear/', views.AseguradoraCreate.as_view(), name='aseguradora_create'),
    path('aseguradoras/<int:pk>/editar/', views.AseguradoraUpdate.as_view(), name='aseguradora_update'),
    path('aseguradoras/<int:pk>/eliminar/', views.AseguradoraDelete.as_view(), name='aseguradora_delete'),

    path('pacientes/', views.PacienteList.as_view(), name='paciente_list'),
    path('pacientes/crear/', views.PacienteCreate.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdate.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', views.PacienteDelete.as_view(), name='paciente_delete'),

    path('medicos/', views.MedicoList.as_view(), name='medico_list'),
    path('medicos/crear/', views.MedicoCreate.as_view(), name='medico_create'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdate.as_view(), name='medico_update'),
    path('medicos/<int:pk>/eliminar/', views.MedicoDelete.as_view(), name='medico_delete'),

    path('medicamentos/', views.MedicamentoList.as_view(), name='medicamento_list'),
    path('medicamentos/crear/', views.MedicamentoCreate.as_view(), name='medicamento_create'),
    path('medicamentos/<int:pk>/editar/', views.MedicamentoUpdate.as_view(), name='medicamento_update'),
    path('medicamentos/<int:pk>/eliminar/', views.MedicamentoDelete.as_view(), name='medicamento_delete'),

    path('tratamientos/', views.TratamientoList.as_view(), name='tratamiento_list'),
    path('tratamientos/crear/', views.TratamientoCreate.as_view(), name='tratamiento_create'),
    path('tratamientos/<int:pk>/editar/', views.TratamientoUpdate.as_view(), name='tratamiento_update'),
    path('tratamientos/<int:pk>/eliminar/', views.TratamientoDelete.as_view(), name='tratamiento_delete'),

    path('consultas/', views.ConsultaList.as_view(), name='consulta_list'),
    path('consultas/crear/', views.ConsultaCreate.as_view(), name='consulta_create'),
    path('consultas/<int:pk>/editar/', views.ConsultaUpdate.as_view(), name='consulta_update'),
    path('consultas/<int:pk>/eliminar/', views.ConsultaDelete.as_view(), name='consulta_delete'),

    path('recetas/', views.RecetaList.as_view(), name='receta_list'),
    path('recetas/crear/', views.RecetaCreate.as_view(), name='receta_create'),
    path('recetas/<int:pk>/editar/', views.RecetaUpdate.as_view(), name='receta_update'),
    path('recetas/<int:pk>/eliminar/', views.RecetaDelete.as_view(), name='receta_delete'),

    path('reserva/enviar/', views.reserva_rapida, name='reserva_rapida'),
]
