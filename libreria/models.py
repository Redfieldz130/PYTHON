from django.db import models

class Equipo(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100,verbose_name='Modelo')
    marca = models.CharField(max_length=100,verbose_name='Marca')
    serial = models.CharField(max_length=100,verbose_name='Serial')
    observaciones = models.CharField(max_length=100,verbose_name='Observaciones')
    tipo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        fila = "Equipo: "  + self.marca + " - " + self.modelo
        return fila
    

    
