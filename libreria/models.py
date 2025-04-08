from django.db import models
from django.utils import timezone



from django.db import models

class Equipo(models.Model):
    TIPOS = [
        ('laptop_pc', 'Laptop/PC'),
        ('celular', 'Celular'),
        ('impresora', 'Impresora'),
        ('monitor', 'Monitor'),
        ('cables', 'cables'),
        ('pc', 'Pc'),
        
        
    ]

    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS, default='laptop_pc')  
    marca = models.CharField(max_length=50)
    serial = models.CharField(max_length=50, unique=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('Asignado', 'Asignado')], default='Disponible')
    mac_address=models.CharField(max_length=17, unique=True, blank=True, null=True)



    def __str__(self):
        return self.modelo


    

    def asignar(self):
        """Método para marcar como Asignado."""
        self.estado = 'Asignado'
        self.save()

    def liberar(self):
        """Método para marcar como Disponible."""
        self.estado = 'Disponible'
        self.save()

    def __str__(self):
        return f"{self.modelo} - {self.marca} ({self.estado})"

    

class Asignacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    colaborador_nombre = models.CharField(max_length=100)
    correo_institucional = models.EmailField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True) 
    fecha_entrega = models.DateField(default=timezone.now)  
    fecha_final = models.DateField(null=True, blank=True)  

    def __str__(self):
        return f"{self.colaborador_nombre} - {self.equipo.modelo} {self.equipo.marca}"

    
