from django.shortcuts import render
from .models import Incidente, Proyecto
from .forms import IncidenteForm, ProyectoForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def lista_incidentes(request):
    incidentes = Incidente.objects.order_by('-fecha')
    return render(request, 'base.html', {
        'incidentes': incidentes
    })


class ProjectListView(ListView):
    model = Proyecto
    template_name = 'pages/projects_list.html'
    context_object_name = 'projects'


class ProjectCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'pages/project_form.html'
    success_url = reverse_lazy('App:projects')

    def form_valid(self, form):
        messages.success(self.request, "Proyecto creado correctamente.")
        return super().form_valid(form)


# Ensure there is at least one project before creating an incidente
class IncidenteCreateView(CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('App:home')

    def dispatch(self, request, *args, **kwargs):
        if not Proyecto.objects.exists():
            messages.info(request, "Debes crear un proyecto antes de crear un incidente.")
            return redirect('App:project_create')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Incidente creado correctamente.")
        return super().form_valid(form)


class IncidenteDetailView(DetailView):
    model = Incidente
    template_name = 'pages/incident_detail.html'
    context_object_name = 'incidente'


class ProjectUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'pages/project_form.html'
    success_url = reverse_lazy('App:projects')

    def form_valid(self, form):
        messages.success(self.request, "Proyecto actualizado correctamente.")
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Proyecto
    template_name = 'pages/project_confirm_delete.html'
    success_url = reverse_lazy('App:projects')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Proyecto eliminado.")
        return super().delete(request, *args, **kwargs)


class IncidenteUpdateView(UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('App:home')

    def form_valid(self, form):
        messages.success(self.request, "Incidente actualizado correctamente.")
        return super().form_valid(form)


class IncidenteDeleteView(DeleteView):
    model = Incidente
    template_name = 'pages/incident_confirm_delete.html'
    success_url = reverse_lazy('App:home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Incidente eliminado.")
        return super().delete(request, *args, **kwargs)
