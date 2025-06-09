from django import template
import json

register = template.Library()
@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))
@register.filter
def json_details(equipo):
    details = {
        'tipo': equipo.get_tipo_display(),
        'marca': equipo.marca,
        'modelo': equipo.modelo,
        'serial': equipo.serial,
        'fecha_compra': equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else '',
        'valor_compra': str(equipo.valor_compra) if equipo.valor_compra else '',
        'ubicacion': equipo.ubicacion,
        'empleado_responsable': equipo.empleado_responsable,
        'proveedor': equipo.proveedor,
        'fecha_fabricacion': equipo.fecha_fabricacion.strftime('%Y-%m-%d') if equipo.fecha_fabricacion else '',
        'vida_util_anios': str(equipo.vida_util_anios) if equipo.vida_util_anios else '',
        'nombre_red': equipo.nombre_red,
        'fecha_recepcion': equipo.fecha_recepcion.strftime('%Y-%m-%d') if equipo.fecha_recepcion else '',
        'fecha_mantenimiento': equipo.fecha_mantenimiento.strftime('%Y-%m-%d') if equipo.fecha_mantenimiento else '',
        'observaciones': equipo.observaciones,
        'mac_address': equipo.mac_address,
        'procesador_marca': equipo.procesador_marca,
        'procesador_velocidad': str(equipo.procesador_velocidad) if equipo.procesador_velocidad else '',
        'procesador_generacion': equipo.procesador_generacion,
        'sistema_operativo': equipo.sistema_operativo,
        'sistema_operativo_version': equipo.sistema_operativo_version,
        'sistema_operativo_bits': equipo.sistema_operativo_bits,
        'almacenamiento_capacidad': str(equipo.almacenamiento_capacidad) if equipo.almacenamiento_capacidad else '',
        'memoria': str(equipo.memoria) if equipo.memoria else '',
        'size_pantalla': str(equipo.size_pantalla) if equipo.size_pantalla else '',
        'resolucion': equipo.resolucion,
        'impresora_tipo': equipo.impresora_tipo,
        'impresora_velocidad_ppm': str(equipo.impresora_velocidad_ppm) if equipo.impresora_velocidad_ppm else '',
        'impresora_color': equipo.impresora_color,
        'impresora_conexion': equipo.impresora_conexion,
        'proyector_lumens': str(equipo.proyector_lumens) if equipo.proyector_lumens else '',
        'ups_vatios': str(equipo.ups_vatios) if equipo.ups_vatios else '',
        'ups_fecha_bateria': equipo.ups_fecha_bateria.strftime('%Y-%m-%d') if equipo.ups_fecha_bateria else '',
        'scanner_velocidad': equipo.scanner_velocidad,
        'scanner_color': equipo.scanner_color,
        'pantalla_proyector_tipo': equipo.pantalla_proyector_tipo,
        'server_numero_procesadores': str(equipo.server_numero_procesadores) if equipo.server_numero_procesadores else '',
        'licencia_tipo': equipo.licencia_tipo,
        'licencia_clase': equipo.licencia_clase,
        'mouse_tipo': equipo.mouse_tipo,
        'mouse_conexion': equipo.mouse_conexion,
        'clase_disco': equipo.clase_disco,
        'cpu_formato_diseno': equipo.cpu_formato_diseno,
    }
    return json.dumps({k: v for k, v in details.items() if v})