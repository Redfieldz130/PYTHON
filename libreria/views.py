from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm, AsignacionForm, CustomUserCreationForm
from .models import Equipo, Asignacion
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from datetime import datetime
from django.utils import timezone
from reportlab.pdfgen import canvas
from docx import Document
from openpyxl import Workbook

def detalle_equipo_json(request, equipo_id):
    equipo = get_object_or_404(Equipo, pk=equipo_id)
    data = {
        'modelo': equipo.modelo,
        'marca': equipo.marca,
        'serial': equipo.serial,
        'mac_address': equipo.mac_address or 'N/A',
        'estado': equipo.estado,
        'observaciones': equipo.observaciones or 'Sin observaciones',
        'tipo': equipo.get_tipo_display(),
        'fecha_fabricacion': equipo.fecha_fabricacion.strftime('%Y-%m-%d') if equipo.fecha_fabricacion else 'N/A',
        'vida_util_anios': equipo.vida_util_anios or 'N/A',
        'nombre_red': equipo.nombre_red or 'N/A',
        'ubicacion': equipo.ubicacion or 'N/A',
        'empleado_responsable': equipo.empleado_responsable or 'N/A',
        'proveedor': equipo.proveedor or 'N/A',
        'valor_compra': str(equipo.valor_compra) if equipo.valor_compra else 'N/A',
        'fecha_compra': equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else 'N/A',
        'fecha_recepcion': equipo.fecha_recepcion.strftime('%Y-%m-%d') if equipo.fecha_recepcion else 'N/A',
        'fecha_mantenimiento': equipo.fecha_mantenimiento.strftime('%Y-%m-%d') if equipo.fecha_mantenimiento else 'N/A',
        'size_pantalla': equipo.size_pantalla or 'N/A',
        'resolucion': equipo.resolucion or 'N/A',
        'procesador_marca': equipo.procesador_marca or 'N/A',
        'procesador_velocidad': equipo.procesador_velocidad or 'N/A',
        'procesador_generacion': equipo.procesador_generacion or 'N/A',
        'sistema_operativo': equipo.sistema_operativo or 'N/A',
        'sistema_operativo_version': equipo.sistema_operativo_version or 'N/A',
        'sistema_operativo_bits': equipo.sistema_operativo_bits or 'N/A',
        'almacenamiento_capacidad': equipo.almacenamiento_capacidad or 'N/A',
        'memoria': equipo.memoria or 'N/A',
        'impresora_tipo': equipo.impresora_tipo or 'N/A',
        'impresora_velocidad_ppm': equipo.impresora_velocidad_ppm or 'N/A',
        'impresora_color': equipo.impresora_color or 'N/A',
        'impresora_conexion': equipo.impresora_conexion or 'N/A',
        'cpu_formato_diseno': equipo.cpu_formato_diseno or 'N/A',
        'proyector_lumens': equipo.proyector_lumens or 'N/A',
        'ups_vatios': equipo.ups_vatios or 'N/A',
        'ups_fecha_bateria': equipo.ups_fecha_bateria.strftime('%Y-%m-%d') if equipo.ups_fecha_bateria else 'N/A',
        'scanner_velocidad': equipo.scanner_velocidad or 'N/A',
        'scanner_color': equipo.scanner_color or 'N/A',
        'pantalla_proyector_tipo': equipo.pantalla_proyector_tipo or 'N/A',
        'server_numero_procesadores': equipo.server_numero_procesadores or 'N/A',
        'licencia_tipo': equipo.licencia_tipo or 'N/A',
        'licencia_clase': equipo.licencia_clase or 'N/A',
        'mouse_tipo': equipo.mouse_tipo or 'N/A',
        'mouse_conexion': equipo.mouse_conexion or 'N/A',
        'clase_disco': equipo.clase_disco or 'N/A',
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

    headers = [
        'ID', 'Tipo', 'Marca', 'Modelo', 'Serial', 'MAC Address', 'Estado', 'Observaciones',
        'Fecha Fabricación', 'Vida Útil (Años)', 'Nombre Red', 'Ubicación', 'Responsable',
        'Proveedor', 'Valor Compra', 'Fecha Compra', 'Fecha Recepción', 'Fecha Mantenimiento',
        'Tamaño Pantalla', 'Resolución', 'Procesador Marca', 'Procesador Velocidad',
        'Procesador Generación', 'Sistema Operativo', 'Versión SO', 'Bits SO',
        'Capacidad Almacenamiento', 'Memoria', 'Tipo Impresora', 'Velocidad Impresora',
        'Color Impresora', 'Conexión Impresora', 'Formato Diseño CPU', 'Lumens Proyector',
        'Vatios UPS', 'Fecha Batería UPS', 'Velocidad Scanner', 'Color Scanner',
        'Tipo Pantalla Proyector', 'Número Procesadores Server', 'Tipo Licencia',
        'Clase Licencia', 'Tipo Mouse', 'Conexión Mouse', 'Clase Disco'
    ]
    worksheet.append(headers)

    for equipo in equipos:
        worksheet.append([
            equipo.id,
            equipo.get_tipo_display(),
            equipo.marca,
            equipo.modelo,
            equipo.serial,
            equipo.mac_address or 'N/A',
            equipo.estado,
            equipo.observaciones or 'Sin observaciones',
            equipo.fecha_fabricacion.strftime('%Y-%m-%d') if equipo.fecha_fabricacion else 'N/A',
            equipo.vida_util_anios or 'N/A',
            equipo.nombre_red or 'N/A',
            equipo.ubicacion or 'N/A',
            equipo.empleado_responsable or 'N/A',
            equipo.proveedor or 'N/A',
            str(equipo.valor_compra) if equipo.valor_compra else 'N/A',
            equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else 'N/A',
            equipo.fecha_recepcion.strftime('%Y-%m-%d') if equipo.fecha_recepcion else 'N/A',
            equipo.fecha_mantenimiento.strftime('%Y-%m-%d') if equipo.fecha_mantenimiento else 'N/A',
            equipo.size_pantalla or 'N/A',
            equipo.resolucion or 'N/A',
            equipo.procesador_marca or 'N/A',
            equipo.procesador_velocidad or 'N/A',
            equipo.procesador_generacion or 'N/A',
            equipo.sistema_operativo or 'N/A',
            equipo.sistema_operativo_version or 'N/A',
            equipo.sistema_operativo_bits or 'N/A',
            equipo.almacenamiento_capacidad or 'N/A',
            equipo.memoria or 'N/A',
            equipo.impresora_tipo or 'N/A',
            equipo.impresora_velocidad_ppm or 'N/A',
            equipo.impresora_color or 'N/A',
            equipo.impresora_conexion or 'N/A',
            equipo.cpu_formato_diseno or 'N/A',
            equipo.proyector_lumens or 'N/A',
            equipo.ups_vatios or 'N/A',
            equipo.ups_fecha_bateria.strftime('%Y-%m-%d') if equipo.ups_fecha_bateria else 'N/A',
            equipo.scanner_velocidad or 'N/A',
            equipo.scanner_color or 'N/A',
            equipo.pantalla_proyector_tipo or 'N/A',
            equipo.server_numero_procesadores or 'N/A',
            equipo.licencia_tipo or 'N/A',
            equipo.licencia_clase or 'N/A',
            equipo.mouse_tipo or 'N/A',
            equipo.mouse_conexion or 'N/A',
            equipo.clase_disco or 'N/A',
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
    equipos_todos = Equipo.objects.all()
    equipos_por_tipo = {tipo[0]: Equipo.objects.filter(tipo=tipo[0]) for tipo in Equipo.TIPOS}

    return render(request, 'Equipos/Index.html', {
        'equipos_todos': equipos_todos,
        **{f'equipos_{tipo[0]}': equipos_por_tipo.get(tipo[0], []) for tipo in Equipo.TIPOS},
    })

def crear_equipos(request):
    if request.method == 'POST':
        formulario = EquipoForm(request.POST)
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
            print(formulario.errors)  # Para depuración, pero los errores ya se mostrarán en el formulario
    else:
        formulario = EquipoForm()
    return render(request, 'Equipos/Crear.html', {'formulario': formulario})

def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    if request.method == 'POST':
        formulario = EquipoForm(request.POST, instance=equipo)
        if formulario.is_valid():
            serial = formulario.cleaned_data['serial']
            if Equipo.objects.filter(serial=serial).exclude(id=equipo_id).exists():
                messages.error(request, "El serial ya está registrado en otro equipo.")
            else:
                formulario.save()
                messages.success(request, f'El equipo "{equipo.modelo}" ha sido actualizado con éxito.')
                return redirect('equipos')
        else:
            messages.error(request, "Error en el formulario. Por favor, revise los campos.")
            print(formulario.errors)
    else:
        formulario = EquipoForm(instance=equipo)
    return render(request, 'Equipos/Editar.html', {'formulario': formulario, 'equipo': equipo})

def asignar(request):
    tipos_equipo = Equipo.objects.values_list('tipo', flat=True).distinct().order_by('tipo')
    equipos_asignados = Asignacion.objects.filter(fecha_final__isnull=True).values_list('equipo_id', flat=True)
    equipos = Equipo.objects.exclude(id__in=equipos_asignados).filter(estado='Disponible')
    asignaciones = Asignacion.objects.all()

    if request.method == 'POST':
        formulario = AsignacionForm(request.POST)
        if formulario.is_valid():
            equipo = formulario.cleaned_data['equipo']
            if Asignacion.objects.filter(equipo=equipo, fecha_final__isnull=True).exists():
                messages.error(request, f'El equipo "{equipo.modelo}" ya está asignado actualmente.')
                return redirect('asignar')
            asignacion = formulario.save()
            equipo.estado = 'Asignado'
            equipo.save()
            messages.success(request, f'El equipo "{equipo.modelo}" ha sido asignado correctamente.')
            return redirect('asignar')
        else:
            messages.error(request, 'Error en el formulario de asignación. Por favor, revise los campos.')
    else:
        formulario = AsignacionForm()
    return render(request, 'Equipos/Asignar.html', {
        'equipos': equipos,
        'asignaciones': asignaciones,
        'tipos_equipo': tipos_equipo,
        'fecha_hoy': timezone.now().date(),
        'formulario': formulario,
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
    messages.success(request, f'El equipo "{equipo.modelo}" ha sido eliminado con éxito.')
    return redirect('equipos')

def liberar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    equipo.estado = "Disponible"
    equipo.save()
    messages.success(request, f'Equipo {equipo.modelo} ahora está disponible.')
    return redirect('equipos')

def registro(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('inicio')
        else:
            messages.error(request, "Error en el formulario de registro. Por favor, revise los campos.")
    else:
        formulario = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': formulario})

def ver_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    equipos = Equipo.objects.all()
    p.drawString(100, 750, "Inventario de Equipos")
    y = 730
    for equipo in equipos:
        p.drawString(100, y, f"{equipo.id} - {equipo.marca} {equipo.modelo} ({equipo.serial})")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
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
    reemplazar_texto(doc, '{{ macaddress }}', mac_address)
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