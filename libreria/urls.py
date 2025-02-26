from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.Inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('equipos/', views.Equipos, name='equipos'),
    path('equipos/crear', views.Crear, name='crear'), 
    path('equipos/crear', views.Editar, name='editar'), 
]
