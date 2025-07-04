# Generated by Django 5.1.6 on 2025-06-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipo',
            options={'verbose_name': 'Equipo', 'verbose_name_plural': 'Equipos'},
        ),
        migrations.AlterField(
            model_name='equipo',
            name='almacenamiento_capacidad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='clase_disco',
            field=models.CharField(blank=True, default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='cpu_formato_diseno',
            field=models.CharField(blank=True, default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='empleado_responsable',
            field=models.CharField(blank=True, default='Sin asignar', max_length=100),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='estado',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Asignado', 'Asignado'), ('En Mantenimiento', 'En Mantenimiento')], default='Disponible', max_length=20),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='impresora_color',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='impresora_conexion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='impresora_tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='impresora_velocidad_ppm',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='licencia_clase',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='licencia_tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='marca',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='memoria',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='mouse_conexion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='mouse_tipo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='pantalla_proyector_tipo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='procesador_generacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='procesador_marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='procesador_velocidad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='proyector_lumens',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='resolucion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='scanner_color',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='scanner_velocidad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='serial',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='server_numero_procesadores',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='sistema_operativo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='sistema_operativo_version',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='size_pantalla',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='tipo',
            field=models.CharField(choices=[('laptop', 'Laptop'), ('impresora', 'Impresora'), ('cpu', 'CPU'), ('monitor', 'Monitor'), ('proyector', 'Proyector'), ('ups', 'UPS'), ('scanner', 'Scanner'), ('pantalla_proyector', 'Pantalla Proyector'), ('tablet', 'Tablet'), ('server', 'Server'), ('router', 'Router'), ('generador_tono', 'Generador de Tono'), ('tester', 'Tester'), ('multimetro', 'Multímetro'), ('access_point', 'Access Point'), ('licencia_informatica', 'Licencia Informática'), ('mouse', 'Mouse'), ('teclado', 'Teclado'), ('headset', 'Headset'), ('bocina', 'Bocina'), ('brazo_monitor', 'Brazo para Monitor'), ('memoria_usb', 'Memoria USB'), ('pointer', 'Pointer'), ('kit_herramientas', 'Kit Herramientas'), ('cartucho', 'Cartucho'), ('toner', 'Toner'), ('botella_tinta', 'Botella Tinta'), ('camara_web', 'Cámara Web'), ('disco_duro', 'Disco Duro')], max_length=50),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='ubicacion',
            field=models.CharField(default='Sin ubicación', max_length=100),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='ups_vatios',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='vida_util_anios',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
