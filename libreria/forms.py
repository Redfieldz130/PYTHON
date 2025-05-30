from django import forms    
from .models import Asignacion,Equipo
from django.contrib.auth.forms import UserCreationForm
import re
from .models import TuModelo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['marca', 'tipo', 'serial', 'modelo', 'observaciones', 'mac_address']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el serial'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese observaciones'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección MAC'}),
        }

    def clean_mac_address(self):
        mac = self.cleaned_data['mac_address']
        
        mac = mac.replace(":", "")  

        if len(mac) != 12 or not re.match(r'^[0-9A-Fa-f]{12}$', mac):
            raise forms.ValidationError("Dirección MAC inválida. Usa el formato XX:XX:XX:XX:XX:XX")

        mac_formatted = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

        return mac_formatted.upper()

    def clean_tipo(self):
        # Esta línea y las siguientes deben estar indentadas 4 espacios más que 'def clean_tipo(self):'
        tipo = self.cleaned_data['tipo']
        # Asegúrate de que esta lista 'tipos_validos' coincida exactamente con la primera parte de las tuplas en models.py
        tipos_validos = ['laptop', 'impresora', 'cpu', 'monitor', 'proyector', 'ups', 'scanner', 'pantalla_proyector', 'tablet', 'server', 'router', 'generador_tono', 'tester', 'multimetro', 'access_point', 'licencia_informatica', 'mouse', 'teclado', 'headset', 'bocina', 'brazo_monitor', 'memoria_usb', 'pointer', 'kit_herramientas', 'cartucho', 'toner', 'botella_tinta', 'camara_web', 'disco_duro', 'p2']
        if tipo not in tipos_validos:
            raise forms.ValidationError(f"'{tipo}' no es un tipo válido.")
        return tipo


class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['colaborador_nombre', 'correo_institucional', 'equipo']
        equipo = forms.ModelChoiceField(queryset=Equipo.objects.all(), empty_label="Seleccione un equipo")

class CustomUserCreationForm(UserCreationForm):
    pass

class TuModeloForm(forms.ModelForm):
    class Meta:
        model = TuModelo
        fields = ['mac_address']

    def clean_mac_address(self):
        mac = self.cleaned_data['mac_address']
        pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        if not re.match(pattern, mac):
            raise forms.ValidationError("Dirección MAC inválida. Usa el formato XX:XX:XX:XX:XX:XX")
        return mac.upper()