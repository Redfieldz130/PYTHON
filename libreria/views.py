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
from django.http import HttpResponse
from openpyxl import Workbook

def detalle_equipo_json(request, equipo_id):
    equipo = get_object_or_404(Equipo, pk=equipo_id)
    data = {
        'modelo': equipo.modelo,
        'marca': equipo.marca,
        'serial': equipo.serial,
        'mac_address': equipo.mac_address,
        'estado': equipo.estado,
        'observaciones': equipo.observaciones,
        'tipo': equipo.tipo,
        'tipo_display': equipo.get_tipo_display()
    }
    return JsonResponse(data)

def eliminar_equipos_seleccionados(request):
    if request.method == 'POST':
        equipo_ids = request.POST.getlist('equipos_seleccionados') 
        equipos = Equipo.objects.filter(id__in=equipo_ids)

        
        if not equipos.exists():
            messages.error(request, 'No se seleccionaron equipos para eliminar.')
            return redirect('equipos')  
       
        equipos.delete()

       
        messages.success(request, 'Los equipos seleccionados fueron eliminados con éxito.')
        return redirect('equipos')  

    return redirect('equipos') 


def exportar_inventario_equipos(request):
    equipos = Equipo.objects.all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Inventario de Equipos"

    
    headers = ['ID', 'Tipo', 'Marca', 'Modelo', 'Serial', 'MAC Address', 'Estado', 'Observaciones']
    worksheet.append(headers)

   
    for equipo in equipos:
        worksheet.append([
            equipo.id,
            equipo.get_tipo_display(),  
            equipo.marca,
            equipo.modelo,
            equipo.serial,
            equipo.mac_address if equipo.mac_address else 'N/A',
            equipo.estado,
            equipo.observaciones if equipo.observaciones else 'Sin observaciones'
        ])

    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=Inventario_Equipos.xlsx'
    workbook.save(response)
    return response

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
    # ... tus filtros existentes
    equipos_laptop = Equipo.objects.filter(tipo='laptop')
    equipos_impresora = Equipo.objects.filter(tipo='impresora')
    equipos_cpu = Equipo.objects.filter(tipo='cpu')
    equipos_monitor = Equipo.objects.filter(tipo='monitor')
    equipos_proyector = Equipo.objects.filter(tipo='proyector')
    equipos_ups = Equipo.objects.filter(tipo='ups')
    equipos_scanner = Equipo.objects.filter(tipo='scanner')
    equipos_pantalla_proyector = Equipo.objects.filter(tipo='pantalla_proyector')
    equipos_tablet = Equipo.objects.filter(tipo='tablet')
    equipos_server = Equipo.objects.filter(tipo='server')
    equipos_router = Equipo.objects.filter(tipo='router')
    equipos_generador_tono = Equipo.objects.filter(tipo='generador_tono')
    equipos_tester = Equipo.objects.filter(tipo='tester')
    equipos_multimetro = Equipo.objects.filter(tipo='multimetro')
    equipos_access_point = Equipo.objects.filter(tipo='access_point')
    equipos_licencia_informatica = Equipo.objects.filter(tipo='licencia_informatica')
    equipos_mouse = Equipo.objects.filter(tipo='mouse')
    equipos_teclado = Equipo.objects.filter(tipo='teclado')
    equipos_headset = Equipo.objects.filter(tipo='headset')
    equipos_bocina = Equipo.objects.filter(tipo='bocina')
    equipos_brazo_monitor = Equipo.objects.filter(tipo='brazo_monitor')
    equipos_memoria_usb = Equipo.objects.filter(tipo='memoria_usb')
    equipos_pointer = Equipo.objects.filter(tipo='pointer')
    equipos_kit_herramientas = Equipo.objects.filter(tipo='kit_herramientas')
    equipos_cartucho = Equipo.objects.filter(tipo='cartucho')
    equipos_toner = Equipo.objects.filter(tipo='toner')
    equipos_botella_tinta = Equipo.objects.filter(tipo='botella_tinta')
    equipos_camara_web = Equipo.objects.filter(tipo='camara_web')
    equipos_disco_duro = Equipo.objects.filter(tipo='disco_duro')
    equipos_p2 = Equipo.objects.filter(tipo='p2')
    equipos_todos = Equipo.objects.all() # Esta ya la tienes

    return render(request, 'Equipos/Index.html', {
        'equipos_laptop': equipos_laptop,
        'equipos_impresora': equipos_impresora,
        'equipos_cpu': equipos_cpu,
        'equipos_monitor': equipos_monitor,
        'equipos_proyector': equipos_proyector,
        'equipos_ups': equipos_ups,
        'equipos_scanner': equipos_scanner,
        'equipos_pantalla_proyector': equipos_pantalla_proyector,
        'equipos_tablet': equipos_tablet,
        'equipos_server': equipos_server,
        'equipos_router': equipos_router,
        'equipos_generador_tono': equipos_generador_tono,
        'equipos_tester': equipos_tester,
        'equipos_multimetro': equipos_multimetro,
        'equipos_access_point': equipos_access_point,
        'equipos_licencia_informatica': equipos_licencia_informatica,
        'equipos_mouse': equipos_mouse,
        'equipos_teclado': equipos_teclado,
        'equipos_headset': equipos_headset,
        'equipos_bocina': equipos_bocina,
        'equipos_brazo_monitor': equipos_brazo_monitor,
        'equipos_memoria_usb': equipos_memoria_usb,
        'equipos_pointer': equipos_pointer,
        'equipos_kit_herramientas': equipos_kit_herramientas,
        'equipos_cartucho': equipos_cartucho,
        'equipos_toner': equipos_toner,
        'equipos_botella_tinta': equipos_botella_tinta,
        'equipos_camara_web': equipos_camara_web,
        'equipos_disco_duro': equipos_disco_duro,
        
        'equipos_todos': equipos_todos,
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
            print(formulario.errors)  
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
        equipo.mac_address = request.POST.get('mac_address')  
        equipo.observaciones = request.POST.get('observaciones')
        equipo.save()
        messages.success(request, f'El equipo "{equipo.modelo}" ha sido actualizado con éxito.')
        return redirect('equipos')
    return render(request, 'equipos/editar.html', {'equipo': equipo})


def asignar(request):
    # Obtener todos los tipos de equipo distintos, independientemente de la disponibilidad
    tipos_equipo = Equipo.objects.values_list('tipo', flat=True).distinct().order_by('tipo')

    equipos_asignados = Asignacion.objects.filter(fecha_final__isnull=True).values_list('equipo_id', flat=True)
    equipos = Equipo.objects.exclude(id__in=equipos_asignados).filter(estado='Disponible')
    asignaciones = Asignacion.objects.all()

    if request.method == 'POST':
        colaborador_nombre = request.POST.get('colaborador_nombre')
        correo_institucional = request.POST.get('correo_institucional')
        equipo_id = request.POST.get('equipo')
        fecha_entrega = request.POST.get('fecha_entrega')
        fecha_final = request.POST.get('fecha_final')

        try:
            equipo = Equipo.objects.get(id=equipo_id)

            if Asignacion.objects.filter(equipo=equipo, fecha_final__isnull=True).exists():
                messages.error(request, f'El equipo "{equipo.modelo}" ya está asignado actualmente.')
                return redirect('asignar')

            fecha_entrega = (
                datetime.strptime(fecha_entrega, "%Y-%m-%d").date()
                if fecha_entrega
                else timezone.now().date()
            )
            fecha_final = (
                datetime.strptime(fecha_final, "%Y-%m-%d").date()
                if fecha_final
                else None
            )

            if fecha_final and fecha_final < fecha_entrega:
                messages.error(request, 'La fecha final no puede ser anterior a la fecha de entrega.')
                return redirect('asignar')

            Asignacion.objects.create(
                colaborador_nombre=colaborador_nombre,
                correo_institucional=correo_institucional,
                equipo=equipo,
                fecha_entrega=fecha_entrega,
                fecha_final=fecha_final
            )

            equipo.estado = 'Disponible' if fecha_final else 'Asignado'
            equipo.save()

            messages.success(request, f'El equipo "{equipo.modelo}" ha sido asignado correctamente.')

        except (Equipo.DoesNotExist, ValueError) as e:
            messages.error(request, f'Error en la asignación: {str(e)}')

        return redirect('asignar')

    return render(request, 'Equipos/Asignar.html', {
        'equipos': equipos,
        'asignaciones': asignaciones,
        'tipos_equipo': tipos_equipo,
        'fecha_hoy': timezone.now().date(),  # Asegúrate de pasar la fecha hoy al contexto
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')

    return render(request, 'registration/login.html')


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
    fecha_entrega = asignacion.fecha_entrega.strftime("%d de %B de %Y")

    fecha_final = asignacion.fecha_final.strftime("%d de %B de %Y") if asignacion.fecha_final else "No aplica"
    mac_address = equipo.mac_address if equipo.mac_address else "No disponible"

    plantilla_path = 'C:/Users/efrain.delacruz/Desktop/PYTHON-1/static/Word.docx'
    doc = Document(plantilla_path)

    reemplazar_texto(doc, '{{ nombreempleado }}', nombre_empleado)
    reemplazar_texto(doc, '{{ equipodescripcion }}', f'{equipo.marca} {equipo.modelo}')
    reemplazar_texto(doc, '{{ equiposerial }}', equipo.serial)
    reemplazar_texto(doc, '{{ macaddress }}', mac_address)  # NUEVO
    reemplazar_texto(doc, '{{ fecha_entrega }}', fecha_entrega)
    reemplazar_texto(doc, '{{ fecha_final }}', fecha_final)

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

