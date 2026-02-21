from django.shortcuts import render

# Create your views here.
from .models import Incidente, Proyecto
from .forms import IncidenteForm, ProyectoForm, IncidenteCompleteForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

def lista_incidentes(request):
    incidentes = Incidente.objects.order_by('-fecha')
    return render(request, 'pages/home.html', {
        'incidentes': incidentes,
        'active_page': 'home',
    })


class ProjectListView(ListView):
    model = Proyecto
    template_name = 'pages/projects_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'projects'
        return context


class ProjectCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'pages/project_form.html'
    success_url = reverse_lazy('App:projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'projects'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Proyecto creado correctamente.")
        return super().form_valid(form)


# Ensure there is at least one project before creating an incidente
class IncidenteCreateView(CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('App:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'incidents'
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'incidents'
        # Formularios embebidos para editar y completar desde el detalle
        context['edit_form'] = IncidenteForm(instance=self.object)
        context['complete_form'] = IncidenteCompleteForm(instance=self.object)
        return context


class ProjectUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'pages/project_form.html'
    success_url = reverse_lazy('App:projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'projects'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Proyecto actualizado correctamente.")
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Proyecto
    template_name = 'pages/project_confirm_delete.html'
    success_url = reverse_lazy('App:projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'projects'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Proyecto eliminado.")
        return super().delete(request, *args, **kwargs)


class IncidenteUpdateView(UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'pages/incident_form.html'
    success_url = reverse_lazy('App:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'incidents'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Incidente actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('App:incident_detail', kwargs={'pk': self.object.pk})


class IncidenteDeleteView(DeleteView):
    model = Incidente
    template_name = 'pages/incident_confirm_delete.html'
    success_url = reverse_lazy('App:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'incidents'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Incidente eliminado.")
        return super().delete(request, *args, **kwargs)


class IncidenteCompleteView(UpdateView):
    model = Incidente
    form_class = IncidenteCompleteForm
    template_name = 'pages/incident_complete.html'
    success_url = reverse_lazy('App:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'incidents'
        return context

    def form_valid(self, form):
        incidente = form.save(commit=False)
        incidente.estado = 'cerrado'
        incidente.save()
        messages.success(self.request, "Incidente marcado como cerrado.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('App:incident_detail', kwargs={'pk': self.object.pk})
