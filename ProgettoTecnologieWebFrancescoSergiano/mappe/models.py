from django.db import models


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

    def __str__(self):
        return f"{self.titolo} ({self.tipo}) - {self.data}"

