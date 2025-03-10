from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm, AsignacionForm
from .models import Equipo, Asignacion
from django.contrib import messages
from django.http import JsonResponse

# Vista para cambiar el estado del equipo
def actualizar_estado(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    # Cambiar el estado del equipo a 'Asignado'
    equipo.estado = 'Asignado'
    equipo.save()

    return JsonResponse({'estado': equipo.estado})
# Vista para la página de inicio
def Inicio(request):
    return render(request, 'Paginas/inicio.html')

# Vista para la página "Nosotros"
def nosotros(request):
    return render(request, 'Paginas/nosotros.html')

# Vista para listar los equipos
def listar_equipos(request):
    estado = request.GET.get('estado', 'todos')
    if estado == 'asignados':
        equipos = Equipo.objects.filter(asignacion__isnull=False)
    elif estado == 'no_asignados':
        equipos = Equipo.objects.filter(asignacion__isnull=True)
    else:
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
def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    if request.method == 'POST':
        equipo.modelo = request.POST.get('modelo')
        equipo.tipo = request.POST.get('tipo')
        equipo.marca = request.POST.get('marca')
        equipo.serial = request.POST.get('serial')
        equipo.observaciones = request.POST.get('observaciones')

        equipo.save()
        messages.success(request, f'El equipo "{equipo.modelo}" ha sido actualizado con éxito.')
        return redirect('editar_equipo', equipo_id=equipo.id)  # Redirigir a la misma página de edición

    return render(request, 'equipos/editar.html', {'equipo': equipo})


# Vista para asignar un equipo a un colaborador

from django.http import JsonResponse

# Vista para asignar un equipo a un colaborador
def asignar(request):
    equipos = Equipo.objects.all()  
    asignaciones = Asignacion.objects.all()  

    if request.method == 'POST':
        colaborador_nombre = request.POST['colaborador_nombre']
        correo_institucional = request.POST['correo_institucional']
        equipo_id = request.POST['equipo']
        equipo = Equipo.objects.get(id=equipo_id)

        # Verifica si el equipo ya está asignado
        if Asignacion.objects.filter(equipo=equipo).exists():
            messages.error(request, f'El equipo "{equipo.modelo}" ya ha sido asignado y no puede ser asignado nuevamente.')
        else:
            # Cambiar el estado del equipo a 'Asignado'
            equipo.estado = 'Asignado'
            equipo.save()

            # Crea la asignación si el equipo no está asignado
            Asignacion.objects.create(
                colaborador_nombre=colaborador_nombre,
                correo_institucional=correo_institucional,
                equipo=equipo
            )
            messages.success(request, f'El equipo "{equipo.modelo}" ha sido asignado con éxito.')

        return redirect('asignar')  # Regresamos a la misma página para evitar la creación de un equipo innecesario

    return render(request, 'Equipos/Asignar.html', {
        'equipos': equipos,
        'asignaciones': asignaciones,
    })


# Vista para mostrar las asignaciones de equipos
def Listadeasignados(request):
    asignaciones = Asignacion.objects.all()  # Obtiene todas las asignaciones
    return render(request, 'Equipos/Listadeasignados.html', {'asignaciones': asignaciones})# Vista para desasignar un equipo
def desasignar(request, id):
    try:
        asignacion = Asignacion.objects.get(id=id)
        equipo = asignacion.equipo
        asignacion.delete()  # Elimina la asignación
        
        # Actualizar el estado del equipo a 'Disponible'
        equipo.estado = "Disponible"
        equipo.save()

        messages.success(request, f'El equipo "{equipo.modelo}" ha sido desasignado correctamente y está disponible ahora.')
    except Asignacion.DoesNotExist:
        messages.error(request, 'No se pudo encontrar la asignación.')
    
    return redirect('asignar')  # Redirige a la página de asignación


def borrar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.delete()
    messages.success(request, f'El equipo "{equipo.modelo}" ha sido eliminado con éxito.')
    return redirect('inventario')  # Redirige a la página de inventario

def liberar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.estado = "Disponible"
    equipo.save()
    messages.success(request, f'Equipo {equipo.modelo} ahora está disponible.')
    return redirect('inventario')
