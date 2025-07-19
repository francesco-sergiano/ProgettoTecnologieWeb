from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Evento(models.Model):
    TIPO_EVENTO = [
        ('FESTA', 'Festa'),
        ('EVENTO', 'Evento'),
        ('ALTRO', 'Altro'),
    ]

    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    luogo = models.CharField(max_length=100)
    data = models.DateField()
    ora = models.TimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_EVENTO)

    latitudine = models.FloatField(default=0.0, help_text="Latitudine in gradi decimali")
    longitudine = models.FloatField(default=0.0, help_text="Longitudine in gradi decimali")

    immagine = models.ImageField(upload_to='eventi/', null=True, blank=True, help_text="Immagine dell'evento")

    prenotabile = models.BooleanField(default=False, help_text="L'evento è prenotabile?")
    contatto = models.CharField(
        max_length=100,
        blank=True,
        help_text="Numero di telefono o email per la prenotazione"
    )

    def __str__(self):
        return f"{self.titolo} ({self.tipo}) - {self.data}"


class Visita(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visita di {self.user} alle {self.timestamp}"

class EventoSalvato(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)
    salvato_il = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'evento')