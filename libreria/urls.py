from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import generar_constancia

urlpatterns = [ 
    path('', views.Inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('inventario/', views.listar_equipos, name='inventario'),
    path('equipos/', views.listar_equipos, name='equipos'),
    path('equipos/crear/', views.crear_equipos, name='crear_equipo'),
    path('equipos/editar/<int:id>/', views.editar_equipo, name='editar_equipo'),
    path('equipos/asignar/', views.asignar, name='asignar'),
    path('equipos/listadeasignados/', views.Listadeasignados, name='listadeasignados'),
    path('desasignar/<int:id>/', views.desasignar, name='desasignar'),
    path('equipo/editar/<int:equipo_id>/', views.editar_equipo, name='editar_equipo'),
    path('equipo/borrar/<int:equipo_id>/', views.borrar_equipo, name='borrar_equipo'),
    path('actualizar_estado/<int:equipo_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/registro/', views.registro, name='registro'),
    path('ver_pdf/', views.ver_pdf, name='ver_pdf'),
    path('generar_constancia/<int:asignacion_id>/', generar_constancia, name='generar_constancia'),
]



