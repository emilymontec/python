from django.contrib import admin
from .models import Proyecto, Incidente

# Register your models here.
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'gravedad', 'estado', 'fecha')
    list_filter = ('gravedad', 'estado', 'fecha')
    search_fields = ('que_paso',)
