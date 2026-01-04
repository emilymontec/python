from django.shortcuts import render, redirect
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

