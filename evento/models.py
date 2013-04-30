from django.db import models

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=120)
    resumen = models.CharField(max_length=200)
    detalle = models.TextField() 
    evento_foto = models.ImageField(upload_to="img_eventos") 
    fecha_inicio = models.DateField("Fecha de inicio")
    fecha_fin = models.DateField("Fecha de fin")
    plazas = models.IntegerField(max_length=3)
    precio_sencillo = models.FloatField() 
    precio_doble = models.FloatField()
    precio_nena = models.FloatField()
    
    def __str__(self):
        return self.question

