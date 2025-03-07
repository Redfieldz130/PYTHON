from django import forms    
from .models import Asignacion,Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['marca', 'tipo', 'serial', 'modelo', 'observaciones']  # Evita '__all__' si prefieres controlarlo
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el serial'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese observaciones'}),
        }
class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['colaborador_nombre', 'correo_institucional', 'equipo']
        equipo = forms.ModelChoiceField(queryset=Equipo.objects.all(), empty_label="Seleccione un equipo")