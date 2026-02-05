from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    

class Incidente(models.Model):

    GRAVEDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_progreso', 'En progreso'),
        ('cerrado', 'Cerrado'),
    ]

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='incidentes'
    )
    que_paso = models.TextField()
    gravedad = models.CharField(max_length=10, choices=GRAVEDAD_CHOICES)
    como_se_arreglo = models.TextField(blank=True)
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='abierto'
    )
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.proyecto} - {self.gravedad} - {self.fecha}"

