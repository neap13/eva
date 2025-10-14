from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from .views import (
    EspecialidadViewSet, AseguradoraViewSet, PacienteViewSet, MedicoViewSet,
    ConsultaViewSet, TratamientoViewSet, MedicamentoViewSet, RecetaViewSet
)

router = routers.DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'aseguradoras', AseguradoraViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'recetas', RecetaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', get_schema_view(
        title="API Salud Vital",
        description="Documentación OpenAPI de la API Salud Vital",
        version="1.0.0",
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='clinica/openapi.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='api-docs'),
]
