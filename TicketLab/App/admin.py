from django.contrib import admin

# Register your models here.
from .models import Proyecto, Incidente

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'gravedad', 'estado', 'fecha')
    list_filter = ('gravedad', 'estado', 'fecha')
    search_fields = ('que_paso',)
