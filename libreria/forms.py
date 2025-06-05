from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Asignacion, Equipo
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo electrónico'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre de usuario'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme contraseña'}),
        }

from django import forms
from .models import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'tipo', 'marca', 'modelo', 'serial', 'observaciones', 'mac_address',
            'fecha_fabricacion', 'vida_util_anios', 'nombre_red', 'ubicacion',
            'empleado_responsable', 'proveedor', 'valor_compra', 'fecha_compra',
            'fecha_recepcion', 'fecha_mantenimiento', 'size_pantalla', 'resolucion',
            'procesador_marca', 'procesador_velocidad', 'procesador_generacion',
            'sistema_operativo', 'sistema_operativo_version', 'sistema_operativo_bits',
            'almacenamiento_capacidad', 'memoria', 'impresora_tipo', 'impresora_velocidad_ppm',
            'impresora_color', 'impresora_conexion', 'cpu_formato_diseno',
            'proyector_lumens', 'ups_vatios', 'ups_fecha_bateria', 'scanner_velocidad',
            'scanner_color', 'pantalla_proyector_tipo', 'server_numero_procesadores',
            'licencia_tipo', 'licencia_clase', 'mouse_tipo', 'mouse_conexion', 'clase_disco',
            'estado'  # Añadido
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el serial'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese observaciones'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 00:1A:2B:3C:4D:5E'}),
            'fecha_fabricacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vida_util_anios': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'nombre_red': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre de red'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese ubicación'}),
            'empleado_responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese responsable'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese proveedor'}),
            'valor_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'size_pantalla': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'resolucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1920x1080'}),
            'procesador_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'procesador_velocidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'procesador_generacion': forms.TextInput(attrs={'class': 'form-control'}),
            'sistema_operativo': forms.TextInput(attrs={'class': 'form-control'}),
            'sistema_operativo_version': forms.TextInput(attrs={'class': 'form-control'}),
            'sistema_operativo_bits': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('32', '32'), ('64', '64'), ('128', '128')]),
            'almacenamiento_capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'memoria': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'impresora_tipo': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('laser', 'Láser'), ('inkjet', 'Inyección de tinta'), ('cartucho', 'Cartucho'), ('botella', 'Botella')]),
            'impresora_velocidad_ppm': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'impresora_color': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('sí', 'Sí'), ('no', 'No')]),
            'impresora_conexion': forms.TextInput(attrs={'class': 'form-control'}),
            'cpu_formato_diseno': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('SFF', 'SFF'), ('MFF', 'MFF'), ('FF', 'FF')]),
            'proyector_lumens': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ups_vatios': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ups_fecha_bateria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scanner_velocidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'scanner_color': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('color', 'Color'), ('bw', 'Blanco y Negro')]),
            'pantalla_proyector_tipo': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('pedestal', 'Pedestal'), ('fija', 'Fija')]),
            'server_numero_procesadores': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'licencia_tipo': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('suscripcion', 'Suscripción'), ('perpetual', 'Perpetua')]),
            'licencia_clase': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('propietaria', 'Propietaria'), ('libre', 'Libre'), ('codigo_abierto', 'Código Abierto')]),
            'mouse_tipo': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('optical', 'Óptico'), ('ball', 'Bola')]),
            'mouse_conexion': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('wired', 'Cableado'), ('wi-fi', 'Inalámbrico')]),
            'clase_disco': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Seleccione'), ('M2', 'M2'), ('SSD', 'SSD'), ('SATA', 'SATA'), ('IDE', 'IDE')]),
            'estado': forms.Select(attrs={'class': 'form-control'}, choices=Equipo.ESTADOS),  # Añadido
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False  # Todos los campos son opcionales por defecto

    def clean_mac_address(self):
        mac = self.cleaned_data.get('mac_address')
        if mac:
            mac = mac.replace(":", "").upper()
            if len(mac) != 12 or not re.match(r'^[0-9A-F]{12}$', mac):
                raise forms.ValidationError("Dirección MAC inválida. Usa el formato XX:XX:XX:XX:XX:XX")
            mac_formatted = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
            return mac_formatted
        return mac

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        tipos_validos = [t[0] for t in Equipo.TIPOS]
        if tipo and tipo not in tipos_validos:
            raise forms.ValidationError(f"'{tipo}' no es un tipo válido.")

        # Validaciones específicas por tipo
        required_fields = {
            'laptop': ['procesador_marca', 'procesador_velocidad', 'memoria', 'almacenamiento_capacidad', 'sistema_operativo'],
            'impresora': ['impresora_tipo', 'impresora_velocidad_ppm', 'impresora_color'],
            'monitor': ['size_pantalla', 'resolucion'],
            'proyector': ['proyector_lumens', 'resolucion'],
            'ups': ['ups_vatios'],
            'scanner': ['scanner_velocidad', 'scanner_color'],
            'pantalla_proyector': ['pantalla_proyector_tipo'],
            'server': ['server_numero_procesadores'],
            'licencia_informatica': ['licencia_tipo', 'licencia_clase'],
            'mouse': ['mouse_tipo', 'mouse_conexion'],
            'disco_duro': ['clase_disco'],
        }

        if tipo in required_fields:
            for field in required_fields[tipo]:
                if not cleaned_data.get(field):
                    self.add_error(field, f"Este campo es obligatorio para {tipo}.")

        return cleaned_data

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['colaborador_nombre', 'correo_institucional', 'equipo']
        widgets = {
            'colaborador_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-select'}),
        }