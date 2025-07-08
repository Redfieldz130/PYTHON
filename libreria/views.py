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
from django.db.models.functions import TruncDate
from django.db.models import DateField
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def historico_equipos(request):
    # Obtener todos los registros ordenados por fecha de eliminación
    historial = HistorialEquipo.objects.all().order_by('-fecha_eliminacion')
    
    # Obtener fechas únicas de eliminación (solo la parte de la fecha)
    fechas_con_registros = HistorialEquipo.objects.annotate(
        fecha_truncada=TruncDate('fecha_eliminacion', output_field=DateField())
    ).values('fecha_truncada').distinct()
    
    # Convertir las fechas a formato YYYY-MM-DD, filtrando None
    fechas_formateadas = [fecha['fecha_truncada'].strftime('%Y-%m-%d') for fecha in fechas_con_registros if fecha['fecha_truncada'] is not None]
    
    # Obtener modelos únicos (excluyendo nulos o vacíos)
    modelos = HistorialEquipo.objects.filter(modelo__isnull=False, modelo__gt='').values('modelo').distinct()
    modelos_formateados = [modelo['modelo'] for modelo in modelos]
    
    # Obtener tipos únicos (excluyendo nulos)
    tipos = HistorialEquipo.objects.filter(tipo__isnull=False).values('tipo').distinct()
    tipos_formateados = []
    for tipo in tipos:
        try:
            # Intentar obtener el nombre legible usando get_tipo_display
            tipo_display = HistorialEquipo.TIPOS[tipo['tipo']][1] if hasattr(HistorialEquipo, 'TIPOS') else tipo['tipo']
        except (KeyError, IndexError):
            tipo_display = tipo['tipo'] or 'Desconocido'
        tipos_formateados.append({'valor': tipo['tipo'], 'display': tipo_display})
    
    # Depuración: Verificar registros con fecha_eliminacion o tipo nulos
    registros_nulos_fecha = HistorialEquipo.objects.filter(fecha_eliminacion__isnull=True)
    if registros_nulos_fecha.exists():
        print(f"Registros con fecha_eliminacion nula: {registros_nulos_fecha.count()}")
        for registro in registros_nulos_fecha:
            print(f"ID: {registro.id}, Marca: {registro.marca}, Modelo: {registro.modelo}, Serial: {registro.serial}, Tipo: {registro.tipo}")
    
    registros_sin_tipo = HistorialEquipo.objects.filter(tipo__isnull=True)
    if registros_sin_tipo.exists():
        print(f"Registros con tipo nulo: {registros_sin_tipo.count()}")
        for registro in registros_sin_tipo:
            print(f"ID: {registro.id}, Marca: {registro.marca}, Modelo: {registro.modelo}, Serial: {registro.serial}, Tipo: {registro.tipo}")
    
    print(f"Total registros: {historial.count()}")
    print(f"Fechas con registros: {fechas_formateadas}")
    print(f"Modelos únicos: {modelos_formateados}")
    print(f"Tipos únicos: {tipos_formateados}")
    for item in historial:
        tipo_display = 'Nulo'
        if item.tipo:
            try:
                tipo_display = item.get_tipo_display() if hasattr(item, 'get_tipo_display') else item.tipo
            except (KeyError, IndexError):
                tipo_display = item.tipo or 'Desconocido'
        print(f"ID: {item.id}, Marca: {item.marca}, Modelo: {item.modelo}, Tipo: {tipo_display}, Fecha: {item.fecha_eliminacion}, Fecha formateada: {item.fecha_eliminacion.date() if item.fecha_eliminacion else 'Nula'}")
    
    return render(request, 'Equipos/historico.html', {
        'historial': historial,
        'fechas_con_registros': fechas_formateadas,
        'modelos': modelos_formateados,
        'tipos': tipos_formateados
    })

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
    categoria = request.GET.get('categoria', 'todos')
    equipos = Equipo.objects.all()
    if categoria != 'todos':
        categorias_dict = {
            'equipos': ['laptop', 'impresora', 'cpu', 'monitor', 'proyector', 'ups', 'scanner', 'pantalla_proyector', 'tablet', 'server', 'router', 'access_point', 'camara_web', 'disco_duro'],
            'accesorios': ['mouse', 'teclado', 'headset', 'bocina', 'brazo_monitor', 'memoria_usb', 'pointer', 'kit_herramientas', 'generador_tono', 'tester', 'multimetro'],
            'licencias': ['licencia_informatica'],
            'materiales': ['cartucho', 'toner', 'botella_tinta'],
        }
        if categoria in categorias_dict:
            equipos = equipos.filter(tipo__in=categorias_dict[categoria])
        else:
            equipos = Equipo.objects.none()
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
    equipos_todos = Equipo.objects.all()
    equipos_categorias = {
        'equipos': ['laptop', 'impresora', 'cpu', 'monitor', 'proyector', 'ups', 'scanner', 'pantalla_proyector', 'tablet', 'server', 'router', 'access_point', 'camara_web', 'disco_duro'],
        'accesorios': ['mouse', 'teclado', 'headset', 'bocina', 'brazo_monitor', 'memoria_usb', 'pointer', 'kit_herramientas', 'generador_tono', 'tester', 'multimetro'],
        'licencias': ['licencia_informatica'],
        'materiales': ['cartucho', 'toner', 'botella_tinta'],
    }
    equipos_por_categoria = {
        'todos': equipos_todos,
        'equipos': equipos_todos.filter(tipo__in=equipos_categorias['equipos']),
        'accesorios': equipos_todos.filter(tipo__in=equipos_categorias['accesorios']),
        'licencias': equipos_todos.filter(tipo__in=equipos_categorias['licencias']),
        'materiales': equipos_todos.filter(tipo__in=equipos_categorias['materiales']),
    }
    asignaciones_dict = {asignacion.equipo.id: asignacion.id for asignacion in Asignacion.objects.filter(fecha_final__isnull=True)}
    print("Asignaciones_dict:", asignaciones_dict)  # Para depuración
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
        print(request.POST)  # Depuración: imprime los datos enviados
        formulario = AsignacionForm(request.POST)
        if formulario.is_valid():
            print(formulario.cleaned_data)  # Depuración: imprime los datos validados
            equipo = formulario.cleaned_data['equipo']
            if Asignacion.objects.filter(equipo=equipo, fecha_final__isnull=True).exists():
                messages.error(request, f'El equipo "{equipo.modelo}" ya está asignado actualmente.')
                return redirect('asignar')
            asignacion = formulario.save()
            print(f"Asignación creada: ID={asignacion.id}, Cédula={asignacion.colaborador_cedula}")  # Depuración
            equipo.estado = 'Asignado'
            equipo.save()
            messages.success(request, f'El equipo "{equipo.modelo}" ha sido asignado a {asignacion.colaborador_nombre} (Cédula: {asignacion.colaborador_cedula}).')
            return redirect('asignar')
        else:
            messages.error(request, 'Error en el formulario de asignación. Por favor, revise los campos.')
            print(formulario.errors)  # Depuración: imprime errores del formulario
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
    print(f"Intentando desasignar asignación con ID: {id}")  # Depuración
    try:
        asignacion = Asignacion.objects.get(id=id)
        equipo = asignacion.equipo
        asignacion.delete()
        equipo.estado = "Disponible"
        equipo.save()
        messages.success(request, f'El equipo "{equipo.modelo}" ha sido desasignado.')
    except Asignacion.DoesNotExist:
        print(f"No se encontró asignación con ID: {id}")  # Depuración
        messages.error(request, 'No se pudo encontrar la asignación.')
    return redirect('equipos')  # Cambiado de 'asignar' a 'equipos'

@require_POST
def borrar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    if request.method == 'POST':
        try:
            # Registrar en historial antes de eliminar (opcional)
            HistorialEquipo.objects.create(
                marca=equipo.marca,
                modelo=equipo.modelo,
                serial=equipo.serial,
                tipo=equipo.tipo,
                fecha_eliminacion=timezone.now(),
                # Agrega aquí otros campos necesarios según tu modelo
            )
            equipo.delete()
            return JsonResponse({'status': 'success', 'message': 'Equipo eliminado correctamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al eliminar el equipo: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

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
    colaborador_cedula = asignacion.colaborador_cedula if asignacion.colaborador_cedula else "No disponible"
    print(f"Colaborador Cedula: '{colaborador_cedula}'")  # Depuración
    plantilla_path = 'C:/Users/efrain.delacruz/Desktop/PYTHON-1/static/Word.docx'
    doc = Document(plantilla_path)
    reemplazar_texto(doc, '{{ nombreempleado }}', nombre_empleado)
    reemplazar_texto(doc, '{{ equipodescripcion }}', f'{equipo.marca} {equipo.modelo}')
    reemplazar_texto(doc, '{{ equiposerial }}', equipo.serial)
    reemplazar_texto(doc, '{{ macaddress }}', mac_address)
    reemplazar_texto(doc, '{{ fecha_entrega }}', fecha_entrega)
    reemplazar_texto(doc, '{{ fecha_final }}', fecha_final)
    reemplazar_texto(doc, '{{ cedulaempleado }}', colaborador_cedula)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=constancia_salida_{equipo.id}.docx'
    doc.save(response)
    return response

def reemplazar_texto(doc, marcador, texto):
    """ Reemplaza texto en el documento, incluyendo párrafos y tablas. """
    texto = str(texto)  # Asegura que el texto sea string
    for p in doc.paragraphs:
        if marcador in p.text:
            print(f"Reemplazando '{marcador}' con '{texto}' en párrafo: {p.text}")  # Depuración
            p.text = p.text.replace(marcador, texto)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if marcador in p.text:
                        print(f"Reemplazando '{marcador}' con '{texto}' en celda: {p.text}")  # Depuración
                        p.text = p.text.replace(marcador, texto)

@csrf_exempt
def asignar_equipo_ajax(request):
    if request.method == 'POST':
        # Procesa los datos del formulario
        # ...
        if equipo_ya_asignado:
            return JsonResponse({'status': 'error', 'message': 'El equipo ya está asignado.'})
        # Si todo está bien:
        return JsonResponse({'status': 'success', 'message': 'Equipo asignado correctamente.'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})