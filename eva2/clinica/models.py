"""
Modelos del dominio Salud Vital (con CHOICES y tabla extra Aseguradora).
"""
from django.db import models

class Especialidad(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.nombre

class Aseguradora(models.Model):
    nombre = models.CharField(max_length=120)
    plan = models.CharField(max_length=120, blank=True)
    def __str__(self): return f"{self.nombre} ({self.plan})" if self.plan else self.nombre

class Paciente(models.Model):
    SEXO_CHOICES = [('M','Masculino'), ('F','Femenino'), ('O','Otro')]
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='O')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self): return f"{self.nombres} {self.apellidos} ({self.rut})"

class Medico(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='medicos')
    registro_colegio = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    def __str__(self): return f"Dr(a). {self.nombres} {self.apellidos} — {self.especialidad}"

class Medicamento(models.Model):
    VIA_CHOICES = [('ORAL','Oral'), ('TOP','Tópica'), ('INJ','Inyectable')]
    nombre = models.CharField(max_length=160, unique=True)
    via_administracion = models.CharField(max_length=4, choices=VIA_CHOICES, default='ORAL')
    indicaciones_generales = models.TextField(blank=True)
    def __str__(self): return self.nombre

class Tratamiento(models.Model):
    TIPO_CHOICES = [('FARM','Farmacológico'), ('FIS','Fisioterapia'), ('PSI','Psicológico'), ('QUIR','Quirúrgico')]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES, default='FARM')
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return f"{self.get_tipo_display()} - {self.paciente}"

class ConsultaMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    diagnostico = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return f"{self.fecha:%Y-%m-%d} {self.paciente} / {self.medico}"

class RecetaMedica(models.Model):
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE, related_name='recetas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dosis = models.CharField(max_length=120)
    frecuencia = models.CharField(max_length=120)
    duracion_dias = models.PositiveIntegerField(default=1)
    indicaciones = models.TextField(blank=True)
    def __str__(self): return f"{self.medicamento} — {self.dosis} / {self.frecuencia}"
