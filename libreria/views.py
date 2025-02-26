from django.shortcuts import render
from django.http import HttpResponse

def Inicio(request):return render(request, 'Paginas/inicio.html')

def nosotros(request):return render(request, 'Paginas/nosotros.html')

def Equipos(request):return render(request, 'Equipos/Index.html')

def Crear(request):return render(request, 'Equipos/Crear.html')

def Editar(request):return render(request, 'Equipos/Editar.html')