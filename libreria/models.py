from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

def validate_mac_address(value):
    """ Valida que el valor sea un MAC address válido. """
    mac_address_regex = re.compile(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')
    if not mac_address_regex.match(value):
        raise ValidationError('El MAC address debe tener el formato correcto (XX:XX:XX:XX:XX:XX).')

class Equipo(models.Model):
    TIPOS = [
        ('laptop', 'Laptop'),
        ('impresora', 'Impresora'),
        ('cpu', 'CPU'),
        ('monitor', 'Monitor'),
        ('proyector', 'Proyector'),
        ('ups', 'UPS'),
        ('scanner', 'Scanner'),
        ('pantalla_proyector', 'Pantalla proyector'),
        ('tablet', 'Tablet'),
        ('server', 'Server'),
        ('router', 'Router'),
        ('generador_tono', 'Generador de tono'),
        ('tester', 'Tester'),
        ('multimetro', 'Multimetro'),
        ('access_point', 'Access point'),
        ('licencia_informatica', 'Licencias informáticas'),
        ('mouse', 'Mouse'),
        ('teclado', 'Teclado'),
        ('headset', 'Headset'),
        ('bocina', 'Bocina'),
        ('brazo_monitor', 'Brazo para monitor'),
        ('memoria_usb', 'Memoria USB'),
        ('pointer', 'Pointer'),
        ('kit_herramientas', 'Kit herramientas'),
        ('cartucho', 'Cartucho'),
        ('toner', 'Toner'),
        ('botella_tinta', 'Botella tinta'),
        ('camara_web', 'Cámara web'),
        ('disco_duro', 'Disco_duro'),
    ]
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS, default='laptop_pc')
    marca = models.CharField(max_length=50)
    serial = models.CharField(max_length=50, unique=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('Asignado', 'Asignado')], default='Disponible')
    mac_address = models.CharField(max_length=17, unique=True, blank=True, null=True, validators=[validate_mac_address])

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

    
def validate_mac(value):
    if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', value):
        raise ValidationError('Formato de MAC inválido (usa XX:XX:XX:XX:XX:XX)')

class TuModelo(models.Model):
    mac_address = models.CharField(max_length=17, validators=[validate_mac])