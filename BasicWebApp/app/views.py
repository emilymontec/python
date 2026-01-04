from django.shortcuts import render, redirect, get_object_or_404
from .models import Mensaje
from .forms import MensajeForm

# Create your views here.
def home(request): # Definir ruta principal
    return render(request, 'home.html')

def about(request): # Definir ruta /about
    return render(request, 'about.html')


def mensajes_view(request):
    mensajes = Mensaje.objects.all().order_by('-creado')
    form = MensajeForm()

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messages')

    return render(request, 'app/messages.html', {
    'mensajes': mensajes,
    'form': form
})

def mensajes_edit(request, id):
    mensaje = get_object_or_404(Mensaje, id=id)

    if request.method == 'POST':
        form = MensajeForm(request.POST, instance=mensaje)
        if form.is_valid():
            form.save()
            return redirect('messages')
    else:
        form = MensajeForm(instance=mensaje)

    return render(request, 'app/edit_message.html', {
        'form': form
    })

def mensajes_delete(request, id):
    mensaje = get_object_or_404(Mensaje, id=id)
    mensaje.delete()
    return redirect('messages')
