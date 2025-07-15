from django.test import TestCase
from mappe.models import Evento
from datetime import date, time

class EventoModelTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            titolo="Concerto",
            descrizione="Un grande concerto in piazza.",
            luogo="Piazza Grande",
            data=date(2025, 7, 20),
            ora=time(21, 0),
            tipo="EVENTO",
            latitudine=44.645,
            longitudine=10.925,
        )

    def test_evento_creazione(self):
        self.assertEqual(Evento.objects.count(), 1)
        evento = Evento.objects.first()
        self.assertEqual(evento.titolo, "Concerto")
        self.assertEqual(evento.tipo, "EVENTO")
        self.assertEqual(evento.latitudine, 44.645)
        self.assertEqual(evento.longitudine, 10.925)

    def test_str_method(self):
        expected_str = "Concerto (EVENTO) - 2025-07-20"
        self.assertEqual(str(self.evento), expected_str)

    def test_valori_di_default(self):
        evento2 = Evento.objects.create(
            titolo="Festa senza coordinate",
            descrizione="Sorpresa",
            luogo="Sala",
            data=date(2025, 8, 1),
            ora=time(20, 0),
            tipo="FESTA",
        )
        self.assertEqual(evento2.latitudine, 0.0)
        self.assertEqual(evento2.longitudine, 0.0)
