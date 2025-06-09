from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm, AsignacionForm, CustomUserCreationForm
from .models import Equipo, Asignacion, HistorialEquipo
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils import timezone
import openpyxl
from docx import Document
from openpyxl.styles import Font

def historico_equipos(request):
    historial = HistorialEquipo.objects.all().order_by('-fecha_eliminacion')  # Ordenar por fecha de eliminación descendente
    return render(request, 'Equipos/historico.html', {'historial': historial})

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

def exportar_excel(request):
    # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario de Tecnología"

    # Definir encabezados
    headers = [
        'Tipo', 'Marca', 'Modelo', 'Serial', 'Estado', 'Ubicación',
        'Fecha de Compra', 'Valor de Compra', 'Empleado Responsable', 'Observaciones'
    ]
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)

    # Obtener todos los equipos
    equipos = Equipo.objects.all()

    # Llenar datos
    for row_num, equipo in enumerate(equipos, 2):
        ws.cell(row=row_num, column=1).value = equipo.get_tipo_display()
        ws.cell(row=row_num, column=2).value = equipo.marca
        ws.cell(row=row_num, column=3).value = equipo.modelo
        ws.cell(row=row_num, column=4).value = equipo.serial
        ws.cell(row=row_num, column=5).value = equipo.estado
        ws.cell(row=row_num, column=6).value = equipo.ubicacion
        ws.cell(row=row_num, column=7).value = equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else ''
        ws.cell(row=row_num, column=8).value = str(equipo.valor_compra) if equipo.valor_compra else ''
        ws.cell(row=row_num, column=9).value = equipo.empleado_responsable
        ws.cell(row=row_num, column=10).value = equipo.observaciones

    # Ajustar el ancho de las columnas
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Preparar la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="Inventario_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    # Guardar el libro en la respuesta
    wb.save(response)
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
    # Obtener todos los equipos
    equipos_todos = Equipo.objects.all()

    # Nueva clasificación por categorías
    equipos_categorias = {
        'equipos': ['laptop', 'impresora', 'cpu', 'monitor', 'proyector', 'ups', 'scanner', 'pantalla_proyector', 'tablet', 'server', 'router', 'access_point', 'camara_web', 'disco_duro'],
        'accesorios': ['mouse', 'teclado', 'headset', 'bocina', 'brazo_monitor', 'memoria_usb', 'pointer', 'kit_herramientas', 'generador_tono', 'tester', 'multimetro'],
        'licencias': ['licencia_informatica'],
        'materiales': ['cartucho', 'toner', 'botella_tinta'],
    }

    # Filtrar equipos por categoría
    equipos_por_categoria = {
        'todos': equipos_todos,
        'equipos': equipos_todos.filter(tipo__in=equipos_categorias['equipos']),
        'accesorios': equipos_todos.filter(tipo__in=equipos_categorias['accesorios']),
        'licencias': equipos_todos.filter(tipo__in=equipos_categorias['licencias']),
        'materiales': equipos_todos.filter(tipo__in=equipos_categorias['materiales']),
    }

    # Crear un diccionario que mapee equipo.id a asignacion.id
    asignaciones_dict = {asignacion.equipo.id: asignacion.id for asignacion in Asignacion.objects.all()}

    context = {
        'equipos_por_categoria': equipos_por_categoria,
        'asignaciones_dict': asignaciones_dict,
    }
    return render(request, 'Equipos/Index.html', context)

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
    if request.method == 'POST':
        historial = HistorialEquipo(
            tipo=equipo.tipo,
            marca=equipo.marca,
            modelo=equipo.modelo,
            serial=equipo.serial,
            usuario_eliminacion=request.user if request.user.is_authenticated else None,
        )
        historial.save()
        Asignacion.objects.filter(equipo=equipo).delete()
        equipo.delete()
        messages.success(request, f"El equipo {equipo.marca} {equipo.modelo} ha sido eliminado correctamente.")
        return redirect('equipos')
    return render(request, 'Equipos/confirmar_eliminacion.html', {'equipo': equipo})

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