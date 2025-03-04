from django.shortcuts import render, redirect
from .forms import EquipoForm
from .models import Equipo
def Inicio(request):
    return render(request, 'Paginas/inicio.html')

def nosotros(request):
    return render(request, 'Paginas/nosotros.html')

def listar_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'Equipos/Index.html', {'equipos': equipos})

def crear_equipos(request):
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_equipos')  # Redirige a la lista de equipos
    else:
        formulario = EquipoForm()

    return render(request, 'Equipos/Crear.html', {'formulario': formulario})

def Editar(request):
    return render(request, 'Equipos/Editar.html')

def Asignar(request):
    return render(request, 'Equipos/Asignar.html')

def Listadeasignados(request):
    return render(request, 'Equipos/Listadeasignados.html')
