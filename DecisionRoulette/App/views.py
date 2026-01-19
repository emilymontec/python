import random
from django.shortcuts import render, redirect
from .models import Opcion

# Create your views here.
def home(request):
    opciones = Opcion.objects.all() # Obtiene todas las opciones de la bd

    if request.method == "POST": # Si el usuario envió un formulario
        texto = request.POST.get("texto") # Captura el campo "texto" del formulario
        if texto: # Si el texto no está vacío
            Opcion.objects.create(texto=texto) # Crea un nuevo registro en la bd
        return redirect("home") # Redirige a la misma página para evitar reenvíos
    # Renderiza la plantilla y pasa las opciones como contexto
    return render(request, "home.html", {"opciones": opciones})


def decidir(request):
    opciones = Opcion.objects.all() # Obtiene todas las opciones
    
    if opciones.exists():
        elegida = random.choice(opciones)
    else:
        elegida = {"texto": "No hay opciones disponibles"}

    # Renderiza la plantilla con la decisión tomada
    return render(request, 'decidir.html', {'elegida': elegida})