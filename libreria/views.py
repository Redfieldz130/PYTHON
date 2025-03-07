from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm, AsignacionForm
from .models import Equipo, Asignacion

# Vista para la página de inicio
def Inicio(request):
    return render(request, 'Paginas/inicio.html')

# Vista para la página "Nosotros"
def nosotros(request):
    return render(request, 'Paginas/nosotros.html')

# Vista para listar los equipos
def listar_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'Equipos/Index.html', {'equipos': equipos})

# Vista para crear un nuevo equipo
def crear_equipos(request):
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()  # Guarda el nuevo equipo
            return redirect('equipos')  # Redirige al listado de equipos
    else:
        formulario = EquipoForm()

    return render(request, 'Equipos/Crear.html', {'formulario': formulario})

# Vista para editar un equipo
def editar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, request.FILES, instance=equipo)
        if formulario.is_valid():
            formulario.save()
            return redirect('equipos')  # Redirige al listado de equipos
    else:
        formulario = EquipoForm(instance=equipo)

    return render(request, 'Equipos/Editar.html', {'formulario': formulario, 'equipo': equipo})

# Vista para asignar un equipo a un colaborador
def asignar(request):
    equipos = Equipo.objects.all()  # Obtén todos los equipos
    asignaciones = Asignacion.objects.all()  # Obtén todas las asignaciones

    if request.method == 'POST':
        colaborador_nombre = request.POST['colaborador_nombre']
        correo_institucional = request.POST['correo_institucional']
        equipo_id = request.POST['equipo']
        equipo = Equipo.objects.get(id=equipo_id)

        # Crea la asignación
        Asignacion.objects.create(
            colaborador_nombre=colaborador_nombre,
            correo_institucional=correo_institucional,
            equipo=equipo
        )

        return redirect('listadeasignados')  # Redirige después de guardar la asignación
    else:
        formulario = AsignacionForm()

    return render(request, 'Equipos/Asignar.html', {
        'equipos': equipos,
        'asignaciones': asignaciones,
    })

# Vista para mostrar las asignaciones de equipos
def Listadeasignados(request):
    asignaciones = Asignacion.objects.all()  # Obtiene todas las asignaciones
    return render(request, 'Equipos/Listadeasignados.html', {'asignaciones': asignaciones})
