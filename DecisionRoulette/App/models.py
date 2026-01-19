from django.db import models

# Create your models here.
class Opcion(models.Model): # Modelo para las opciones de la ruleta
    texto = models.CharField(max_length=200)
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self): # mostrar el objeto como texto
        return self.texto # Imprime el texto de la opción
