from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    # Agrega campos adicionales aquí si es necesario
    pass


class CachedLocation(models.Model):
    query = models.CharField(max_length=255, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    display_name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('query', 'display_name')

    def __str__(self):
        return f"{self.query} → {self.display_name}"

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    location = models.CharField(max_length=100, verbose_name="Ubicación")
    origin = models.CharField(max_length=255, verbose_name="Dirección de recogida")
    destination = models.CharField(max_length=255, verbose_name="Dirección de destino")
    phone = models.CharField(max_length=15, verbose_name="Teléfono")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    time = models.CharField(
        max_length=50,
        choices=[
            ('morning', 'Morning (8AM - 12PM)'),
            ('afternoon', 'Afternoon (12PM - 4PM)'),
            ('evening', 'Evening (4PM - 8PM)')
        ],
        verbose_name="Hora preferida"
    )
    date = models.DateField(verbose_name="Fecha de mudanza")
    size = models.CharField(
        max_length=50,
        choices=[
            ('studio', 'Studio Apartment'),
            ('1bed', '1-Bedroom'),
            ('2bed', '2-Bedroom'),
            ('3bed', '3-Bedroom'),
            ('4bed', '4-Bedroom+')
        ],
        verbose_name="Tamaño de la vivienda"
    )
    helpers = models.PositiveIntegerField(verbose_name="Número de ayudantes")
    special_item = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Artículos especiales"
    )

    # Representación del modelo
    def __str__(self):
        return f"{self.name} - {self.date} - {self.origin} to {self.destination}"
    
    
class ContactShort(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electrónico")
    date = models.DateField(verbose_name="Fecha")
    message = models.CharField(max_length=500, verbose_name="Mensaje")
    
    # Representación del modelo
    def __str__(self):
        return f"{self.name} - {self.date} - {self.email}"
    
    