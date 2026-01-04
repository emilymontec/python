from django.db import models

# Create your models here.
class Mensaje(models.Model): # Modelo BD de mensajes
    texto = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto[:30]
