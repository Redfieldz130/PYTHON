from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Inventario IDEICE</h1>")
def nosotros(request):
    return render(request, 'Paginas/nosotros.html')
