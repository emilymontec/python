from django.shortcuts import render
from .models import Incidente
from .forms import IncidenteForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def lista_incidentes(request):
    incidentes = Incidente.objects.order_by('-fecha')
    return render(request, 'pages/home.html', {
        'incidentes': incidentes
    })


class IncidenteDetailView(DetailView):
    model = Incidente
    template_name = 'pages/incident_detail.html'
    context_object_name = 'incidente'


class IncidenteCreateView(CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('lista_incidentes')

    def form_valid(self, form):
        messages.success(self.request, "Incidente creado correctamente.")
        return super().form_valid(form)


class IncidenteUpdateView(UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('lista_incidentes')

    def form_valid(self, form):
        messages.success(self.request, "Incidente actualizado correctamente.")
        return super().form_valid(form)


class IncidenteDeleteView(DeleteView):
    model = Incidente
    template_name = 'pages/incident_confirm_delete.html'
    success_url = reverse_lazy('lista_incidentes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Incidente eliminado.")
        return super().delete(request, *args, **kwargs)
