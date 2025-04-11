from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm, CustomUserCreationForm
from .models import Equipo, Asignacion
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from datetime import datetime
from django.utils import timezone
from reportlab.pdfgen import canvas

from docx import Document

def actualizar_estado(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.estado = 'Asignado'
    equipo.save()
    return JsonResponse({'estado': equipo.estado})

def Inicio(request):
    return render(request, 'Paginas/inicio.html')

def nosotros(request):
    return render(request, 'Paginas/nosotros.html')

def listar_equipos(request):
    equipos_laptop = Equipo.objects.filter(tipo='Laptop_pc')
    equipos_celular = Equipo.objects.filter(tipo='Celular')
    equipos_impresora = Equipo.objects.filter(tipo='Impresora')
    equipos_monitor = Equipo.objects.filter(tipo='Monitor')
    equipos_pc = Equipo.objects.filter(tipo='Pc')
    equipos_cables = Equipo.objects.filter(tipo='cables')

    # Debug: Mostrar los equipos encontrados en consola
    print("Laptops:", list(equipos_laptop.values()))
    print("Celulares:", list(equipos_celular.values()))
    print("Impresoras:", list(equipos_impresora.values()))
    print("Monitores:", list(equipos_monitor.values()))
    print("cables:", list(equipos_cables.values()))
    print("pc:", list(equipos_pc.values()))

    return render(request, 'Equipos/Index.html', {
        'equipos_laptop': equipos_laptop,
        'equipos_celular': equipos_celular,
        'equipos_impresora': equipos_impresora,
        'equipos_monitor': equipos_monitor,
        'equipos_pc': equipos_pc,
        'equipos_cables': equipos_cables,
    })

def crear_equipos(request):
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, request.FILES)
        if formulario.is_valid():
            serial = formulario.cleaned_data['serial']
            if Equipo.objects.filter(serial=serial).exists():
                messages.error(request, "El serial ya está registrado.")
            else:
                formulario.save()
                messages.success(request, "Equipo agregado exitosamente.")
                return redirect('equipos')
        else:
            messages.error(request, "Error en el formulario. Por favor, revise los campos.")
            print(formulario.errors)  # Esto te permitirá ver qué errores se están generando en el servidor.
    else:
        formulario = EquipoForm()
    return render(request, 'Equipos/Crear.html', {'formulario': formulario})


def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    if request.method == 'POST':
        equipo.modelo = request.POST.get('modelo')
        equipo.tipo = request.POST.get('tipo')
        equipo.marca = request.POST.get('marca')
        equipo.serial = request.POST.get('serial')
        equipo.mac_address = request.POST.get('mac_address')  # Agregar el campo MAC Address
        equipo.observaciones = request.POST.get('observaciones')
        equipo.save()
        messages.success(request, f'El equipo "{equipo.modelo}" ha sido actualizado con éxito.')
        return redirect('equipos')
    return render(request, 'equipos/editar.html', {'equipo': equipo})


def asignar(request):
    equipos = Equipo.objects.all()
    asignaciones = Asignacion.objects.all()
    
    if request.method == 'POST':
        colaborador_nombre = request.POST.get('colaborador_nombre')
        correo_institucional = request.POST.get('correo_institucional')
        equipo_id = request.POST.get('equipo')
        fecha_entrega = request.POST.get('fecha_entrega')  # Nuevo campo
        fecha_final = request.POST.get('fecha_final')
        
        try:
            equipo = Equipo.objects.get(id=equipo_id)
            
            if Asignacion.objects.filter(equipo=equipo).exists():
                messages.error(request, f'El equipo "{equipo.modelo}" ya está asignado.')
            else:
                # Validar y convertir fechas
                fecha_entrega = (
                    datetime.strptime(fecha_entrega, "%Y-%m-%d").date() 
                    if fecha_entrega 
                    else timezone.now().date()  # Fallback a fecha actual
                )
                fecha_final = (
                    datetime.strptime(fecha_final, "%Y-%m-%d").date() 
                    if fecha_final 
                    else None
                )
                
                # Validar que fecha_final no sea anterior a fecha_entrega
                if fecha_final and fecha_final < fecha_entrega:
                    messages.error(request, 'La fecha final no puede ser anterior a la fecha de entrega.')
                    return redirect('asignar')
                
                # Asignar equipo y guardar
                equipo.estado = 'Asignado'
                equipo.save()
                
                Asignacion.objects.create(
                    colaborador_nombre=colaborador_nombre,
                    correo_institucional=correo_institucional,
                    equipo=equipo,
                    fecha_entrega=fecha_entrega,  # Usa la fecha del formulario
                    fecha_final=fecha_final
                )
                messages.success(request, f'El equipo "{equipo.modelo}" ha sido asignado.')
                
        except (Equipo.DoesNotExist, ValueError) as e:
            messages.error(request, f'Error en la asignación: {str(e)}')
        
        return redirect('asignar')
    
    return render(request, 'Equipos/Asignar.html', {
        'equipos': equipos, 
        'asignaciones': asignaciones
    })
def Listadeasignados(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'Equipos/Listadeasignados.html', {'asignaciones': asignaciones})

def desasignar(request, id):
    try:
        asignacion = Asignacion.objects.get(id=id)
        equipo = asignacion.equipo
        asignacion.delete()
        equipo.estado = "Disponible"
        equipo.save()
        messages.success(request, f'El equipo "{equipo.modelo}" ha sido desasignado.')
    except Asignacion.DoesNotExist:
        messages.error(request, 'No se pudo encontrar la asignación.')
    return redirect('asignar')

def borrar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.delete()
    messages.success(request, f'El equipo "{equipo.modelo}" ha sido eliminado con exito.')
    return redirect('inventario')

def liberar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.estado = "Disponible"
    equipo.save()
    messages.success(request, f'Equipo {equipo.modelo} ahora está disponible.')
    return redirect('inventario')

def registro(request):
    data = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('inicio')
        data['form'] = formulario
    return render(request, 'registration/registro.html', data)

def ver_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    equipos = Equipo.objects.all()
    p.drawString(100, 750, "Inventario de Equipos")
    for i, equipo in enumerate(equipos):
        p.drawString(100, 730 - i * 20, f"{equipo.id} - {equipo.modelo}")
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="inventario.pdf"'
    return response

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "¡Bienvenido!")
            return redirect("inicio")
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")
def inicio_view(request):
    
    return render(request, "inicio.html")
def generar_constancia(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)

    nombre_empleado = asignacion.colaborador_nombre
    equipo = asignacion.equipo
    fecha_entrega = asignacion.fecha_entrega.strftime("%d de %B de %Y")  # Formato: 04 de abril de 2025

    # Si fecha_final es None, asigna "No aplica" en su lugar
    fecha_final = asignacion.fecha_final.strftime("%d de %B de %Y") if asignacion.fecha_final else "No aplica"

    plantilla_path = 'C:/Users/efrain.delacruz/Desktop/PYTHON-1/static/Word.docx'
    doc = Document(plantilla_path)

    reemplazar_texto(doc, '{{ nombreempleado }}', nombre_empleado)
    reemplazar_texto(doc, '{{ equipodescripcion }}', f'{equipo.marca} {equipo.modelo}')
    reemplazar_texto(doc, '{{ equiposerial }}', equipo.serial)
    reemplazar_texto(doc, '{{ fecha_entrega }}', fecha_entrega)
    reemplazar_texto(doc, '{{ fecha_final }}', fecha_final)  # Ahora maneja correctamente la fecha final

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=constancia_salida_{equipo.id}.docx'
    doc.save(response)

    return response




def reemplazar_texto(doc, marcador, texto):
    """ Reemplaza texto en el documento, incluyendo párrafos y tablas. """
    for p in doc.paragraphs:
        if marcador in p.text:
            for run in p.runs:
                run.text = run.text.replace(marcador, texto)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if marcador in p.text:
                        for run in p.runs:
                            run.text = run.text.replace(marcador, texto)

