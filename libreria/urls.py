from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.Inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('equipos/', views.listar_equipos, name='equipos'),
    path('equipos/crear/', views.crear_equipos, name='crear_equipo'),
    path('equipos/editar/<int:id>/', views.editar_equipo, name='editar_equipo'),
    path('equipos/asignar/', views.asignar, name='asignar'),
    path('equipos/listadeasignados/', views.Listadeasignados, name='listadeasignados'),
]
