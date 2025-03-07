from django.shortcuts import render, redirect, get_object_or_404
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
        formulario = EquipoForm(request.POST, request.FILES)  # No necesitas `or None`
        if formulario.is_valid():
            formulario.save()  # Guarda los datos en la BD
            return redirect('equipos')  # Redirige al listado de equipos
    else:
        formulario = EquipoForm()

    return render(request, 'Equipos/Crear.html', {'formulario': formulario})

def editar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, request.FILES, instance=equipo)
        if formulario.is_valid():
            formulario.save()
            return redirect('equipos')  # Redirige a la lista de equipos
    else:
        formulario = EquipoForm(instance=equipo)

    return render(request, 'Equipos/Editar.html', {'formulario': formulario, 'equipo': equipo})

def asignar(request):
    return render(request, 'Equipos/Asignar.html')

def Listadeasignados(request):
    return render(request, 'Equipos/Listadeasignados.html')
