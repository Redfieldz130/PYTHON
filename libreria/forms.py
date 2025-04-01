from django import forms    
from .models import Asignacion,Equipo
from django.contrib.auth.forms import UserCreationForm

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['marca', 'tipo', 'serial', 'modelo', 'observaciones']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el serial'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese observaciones'}),
        }


    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        tipos_validos = ['laptop_pc', 'celular', 'imprecsora', 'monitor','cables','pc' ]  
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
