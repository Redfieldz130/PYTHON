from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.Inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('equipos/', views.listar_equipos, name='equipos'),
    path('equipos/crear/', views.crear_equipos, name='crear'),  # Asegúrate de usar la barra diagonal aquí
    path('equipos/editar/<int:id>/', views.Editar, name='editar'),  # Corregir la ruta de editar (con parámetro)
    path('equipos/asignar/', views.Asignar, name='asignar'),
    path('equipos/listadeasignados/', views.Listadeasignados, name='listadeasignados'),
]

