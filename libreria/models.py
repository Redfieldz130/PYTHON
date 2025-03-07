from django.db import models
from django.utils import timezone



class Equipo(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    marca = models.CharField(max_length=100, verbose_name='Marca')
    serial = models.CharField(max_length=100, unique=True, verbose_name='Serial')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')  # Cambiado a TextField
    tipo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo')

class Asignacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    colaborador_nombre = models.CharField(max_length=100)
    correo_institucional = models.EmailField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.colaborador_nombre} - {self.equipo.nombre}"
    
