"""
Vistas HTML + API (DRF) + Home con Reserva Rápida.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica, Aseguradora
)
from .forms import (
    EspecialidadForm, PacienteForm, MedicoForm, ConsultaForm,
    TratamientoForm, MedicamentoForm, RecetaForm, AseguradoraForm, ReservaRapidaForm
)
from .filters import (
    MedicoFilter, PacienteFilter, ConsultaFilter, TratamientoFilter,
    MedicamentoFilter, RecetaFilter
)

# =============== HOME + RESERVA RÁPIDA ===============
def home(request):
    form = ReservaRapidaForm()
    context = {
        "reserva_form": form,
        "whatsapp_number": "56912345678",  # CAMBIA AL TUYO
        "wa_text": "Hola, quiero reservar una hora en Salud Vital."
    }
    return render(request, "clinica/home.html", context)

@transaction.atomic
def reserva_rapida(request):
    if request.method != "POST":
        return redirect("/")

    form = ReservaRapidaForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Revisa el formulario; hay campos inválidos.")
        return redirect("/#reserva")

    data = form.cleaned_data
    paciente, _ = Paciente.objects.get_or_create(
        rut=data["rut"],
        defaults={
            "nombres": data["nombres"],
            "apellidos": data["apellidos"],
            "email": data["email"],
            "telefono": data["telefono"],
        },
    )
    paciente.nombres = data["nombres"]; paciente.apellidos = data["apellidos"]
    paciente.email = data["email"]; paciente.telefono = data["telefono"]; paciente.save()

    esp = data["especialidad"]
    medico = Medico.objects.filter(especialidad=esp).order_by("id").first() or Medico.objects.order_by("id").first()
    if not medico:
        messages.error(request, "No hay médicos disponibles aún. Intenta más tarde.")
        return redirect("/#reserva")

    ConsultaMedica.objects.create(
        paciente=paciente, medico=medico, especialidad=esp,
        fecha=data["fecha"], motivo=data.get("motivo") or "Reserva web",
        diagnostico="", precio=0
    )
    messages.success(request, "¡Listo! Tu solicitud de reserva fue registrada.")
    return redirect("/#reserva")

# =============== LISTAS (HTML) ===============
class EspecialidadList(ListView):
    model = Especialidad; template_name = "clinica/especialidad_list.html"; paginate_by = 10

class AseguradoraList(ListView):
    model = Aseguradora; template_name = "clinica/aseguradora_list.html"; paginate_by = 10

class PacienteList(ListView):
    model = Paciente; template_name = "clinica/paciente_list.html"; paginate_by = 10
    def get_queryset(self):
        q = self.request.GET.get("q")
        qs = super().get_queryset().select_related("aseguradora")
        return qs.filter(Q(nombres__icontains=q)|Q(apellidos__icontains=q)|Q(rut__icontains=q)) if q else qs

class MedicoList(ListView):
    model = Medico; template_name = "clinica/medico_list.html"; paginate_by = 10
    def get_queryset(self):
        esp = self.request.GET.get("especialidad")
        qs = super().get_queryset().select_related("especialidad")
        return qs.filter(especialidad_id=esp) if esp else qs

class ConsultaList(ListView):
    model = ConsultaMedica; template_name = "clinica/consulta_list.html"; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente","medico","especialidad")
        med = self.request.GET.get("medico"); pac = self.request.GET.get("paciente"); esp = self.request.GET.get("especialidad")
        if med: qs = qs.filter(medico_id=med)
        if pac: qs = qs.filter(paciente_id=pac)
        if esp: qs = qs.filter(especialidad_id=esp)
        return qs.order_by("-fecha")

class TratamientoList(ListView):
    model = Tratamiento; template_name = "clinica/tratamiento_list.html"; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente","medico")
        t = self.request.GET.get("tipo")
        return qs.filter(tipo=t) if t else qs

class MedicamentoList(ListView):
    model = Medicamento; template_name = "clinica/medicamento_list.html"; paginate_by = 10

class RecetaList(ListView):
    model = RecetaMedica; template_name = "clinica/receta_list.html"; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset().select_related("consulta","medicamento")
        med = self.request.GET.get("medicamento")
        return qs.filter(medicamento_id=med) if med else qs

# Formularios genéricos (crear/editar/eliminar)
class EspecialidadCreate(CreateView): model=Especialidad; form_class=EspecialidadForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("especialidad_list")
class EspecialidadUpdate(UpdateView): model=Especialidad; form_class=EspecialidadForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("especialidad_list")
class EspecialidadDelete(DeleteView): model=Especialidad; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("especialidad_list")

class AseguradoraCreate(CreateView): model=Aseguradora; form_class=AseguradoraForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("aseguradora_list")
class AseguradoraUpdate(UpdateView): model=Aseguradora; form_class=AseguradoraForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("aseguradora_list")
class AseguradoraDelete(DeleteView): model=Aseguradora; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("aseguradora_list")

class PacienteCreate(CreateView): model=Paciente; form_class=PacienteForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("paciente_list")
class PacienteUpdate(UpdateView): model=Paciente; form_class=PacienteForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("paciente_list")
class PacienteDelete(DeleteView): model=Paciente; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("paciente_list")

class MedicoCreate(CreateView): model=Medico; form_class=MedicoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("medico_list")
class MedicoUpdate(UpdateView): model=Medico; form_class=MedicoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("medico_list")
class MedicoDelete(DeleteView): model=Medico; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("medico_list")

class MedicamentoCreate(CreateView): model=Medicamento; form_class=MedicamentoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("medicamento_list")
class MedicamentoUpdate(UpdateView): model=Medicamento; form_class=MedicamentoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("medicamento_list")
class MedicamentoDelete(DeleteView): model=Medicamento; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("medicamento_list")

class TratamientoCreate(CreateView): model=Tratamiento; form_class=TratamientoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("tratamiento_list")
class TratamientoUpdate(UpdateView): model=Tratamiento; form_class=TratamientoForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("tratamiento_list")
class TratamientoDelete(DeleteView): model=Tratamiento; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("tratamiento_list")

class ConsultaCreate(CreateView): model=ConsultaMedica; form_class=ConsultaForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("consulta_list")
class ConsultaUpdate(UpdateView): model=ConsultaMedica; form_class=ConsultaForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("consulta_list")
class ConsultaDelete(DeleteView): model=ConsultaMedica; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("consulta_list")

class RecetaCreate(CreateView): model=RecetaMedica; form_class=RecetaForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("receta_list")
class RecetaUpdate(UpdateView): model=RecetaMedica; form_class=RecetaForm; template_name="clinica/object_form.html"; success_url=reverse_lazy("receta_list")
class RecetaDelete(DeleteView): model=RecetaMedica; template_name="clinica/confirm_delete.html"; success_url=reverse_lazy("receta_list")

# =============== API (DRF) ===============
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

class EspecialidadViewSet(BaseViewSet):
    queryset = Especialidad.objects.all().order_by("nombre")
    from .serializers import EspecialidadSerializer
    serializer_class = EspecialidadSerializer
    search_fields = ["nombre"]; ordering_fields = ["nombre"]

class AseguradoraViewSet(BaseViewSet):
    queryset = Aseguradora.objects.all().order_by("nombre")
    from .serializers import AseguradoraSerializer
    serializer_class = AseguradoraSerializer
    search_fields = ["nombre","plan"]; ordering_fields = ["nombre"]

class PacienteViewSet(BaseViewSet):
    queryset = Paciente.objects.select_related("aseguradora").all().order_by("apellidos","nombres")
    from .serializers import PacienteSerializer
    serializer_class = PacienteSerializer
    filterset_class = PacienteFilter
    search_fields = ["rut","nombres","apellidos","email","telefono"]
    ordering_fields = ["apellidos","nombres","rut"]

class MedicoViewSet(BaseViewSet):
    queryset = Medico.objects.select_related("especialidad").all().order_by("apellidos","nombres")
    from .serializers import MedicoSerializer
    serializer_class = MedicoSerializer
    filterset_class = MedicoFilter
    search_fields = ["rut","nombres","apellidos","email","telefono","especialidad__nombre"]
    ordering_fields = ["apellidos","nombres"]

class MedicamentoViewSet(BaseViewSet):
    queryset = Medicamento.objects.all().order_by("nombre")
    from .serializers import MedicamentoSerializer
    serializer_class = MedicamentoSerializer
    filterset_class = MedicamentoFilter
    search_fields = ["nombre"]; ordering_fields = ["nombre"]

class TratamientoViewSet(BaseViewSet):
    queryset = Tratamiento.objects.select_related("paciente","medico").all().order_by("-fecha_inicio")
    from .serializers import TratamientoSerializer
    serializer_class = TratamientoSerializer
    filterset_class = TratamientoFilter
    search_fields = ["descripcion","paciente__nombres","paciente__apellidos","medico__apellidos"]
    ordering_fields = ["fecha_inicio","fecha_fin"]

class ConsultaViewSet(BaseViewSet):
    queryset = ConsultaMedica.objects.select_related("paciente","medico","especialidad").all().order_by("-fecha")
    from .serializers import ConsultaSerializer
    serializer_class = ConsultaSerializer
    filterset_class = ConsultaFilter
    search_fields = ["motivo","diagnostico","paciente__apellidos","medico__apellidos","especialidad__nombre"]
    ordering_fields = ["fecha","precio"]

class RecetaViewSet(BaseViewSet):
    queryset = RecetaMedica.objects.select_related("consulta","medicamento").all().order_by("-id")
    from .serializers import RecetaSerializer
    serializer_class = RecetaSerializer
    filterset_class = RecetaFilter
    search_fields = ["medicamento__nombre","indicaciones"]
    ordering_fields = ["duracion_dias"]
