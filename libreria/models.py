from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

def validate_mac_address(value):
    """Valida que el valor sea un MAC address válido."""
    if value:  # Permitir vacío porque es opcional
        mac_address_regex = re.compile(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')
        if not mac_address_regex.match(value):
            raise ValidationError('El MAC address debe tener el formato XX:XX:XX:XX:XX:XX.')

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
        ('disco_duro', 'Disco duro'),
    ]

    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    marca = models.CharField(max_length=50)
    serial = models.CharField(max_length=50, unique=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('Asignado', 'Asignado')], default='Disponible')
    mac_address = models.CharField(max_length=17, blank=True, null=True, validators=[validate_mac_address])
    # Campos comunes de la matriz
    fecha_fabricacion = models.DateField(blank=True, null=True)
    vida_util_anios = models.IntegerField(blank=True, null=True)
    nombre_red = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    empleado_responsable = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    fecha_recepcion = models.DateField(blank=True, null=True)
    fecha_mantenimiento = models.DateField(blank=True, null=True)
    # Campos específicos por tipo
    size_pantalla = models.FloatField(blank=True, null=True)
    resolucion = models.CharField(max_length=20, blank=True, null=True)
    procesador_marca = models.CharField(max_length=50, blank=True, null=True)
    procesador_velocidad = models.FloatField(blank=True, null=True)
    procesador_generacion = models.CharField(max_length=20, blank=True, null=True)
    sistema_operativo = models.CharField(max_length=50, blank=True, null=True)
    sistema_operativo_version = models.CharField(max_length=20, blank=True, null=True)
    sistema_operativo_bits = models.CharField(max_length=10, blank=True, null=True)
    almacenamiento_capacidad = models.IntegerField(blank=True, null=True)
    memoria = models.IntegerField(blank=True, null=True)
    impresora_tipo = models.CharField(max_length=20, blank=True, null=True)
    impresora_velocidad_ppm = models.IntegerField(blank=True, null=True)
    impresora_color = models.CharField(max_length=3, blank=True, null=True)
    impresora_conexion = models.CharField(max_length=20, blank=True, null=True)
    cpu_formato_diseno = models.CharField(max_length=10, blank=True, null=True)
    proyector_lumens = models.IntegerField(blank=True, null=True)
    ups_vatios = models.IntegerField(blank=True, null=True)
    ups_fecha_bateria = models.DateField(blank=True, null=True)
    scanner_velocidad = models.IntegerField(blank=True, null=True)
    scanner_color = models.CharField(max_length=10, blank=True, null=True)
    pantalla_proyector_tipo = models.CharField(max_length=20, blank=True, null=True)
    server_numero_procesadores = models.IntegerField(blank=True, null=True)
    licencia_tipo = models.CharField(max_length=20, blank=True, null=True)
    licencia_clase = models.CharField(max_length=20, blank=True, null=True)
    mouse_tipo = models.CharField(max_length=20, blank=True, null=True)
    mouse_conexion = models.CharField(max_length=20, blank=True, null=True)
    clase_disco = models.CharField(max_length=10, blank=True, null=True)

    def asignar(self):
        """Método para marcar como Asignado."""
        self.estado = 'Asignado'
        self.save()

    def liberar(self):
        """Método para marcar como Disponible."""
        self.estado = 'Disponible'
        self.save()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.serial})"

class Asignacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    colaborador_nombre = models.CharField(max_length=100)
    correo_institucional = models.EmailField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(default=timezone.now)
    fecha_final = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.colaborador_nombre} - {self.equipo.marca} {self.equipo.modelo}"