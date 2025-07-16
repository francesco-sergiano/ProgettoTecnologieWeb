from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from models import Evento
from datetime import date, time

class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.staff = User.objects.create_user(username='staff', password='pass', is_staff=True)
        self.superuser = User.objects.create_superuser(username='super', password='pass')
        self.evento = Evento.objects.create(
            titolo="Test Evento",
            data=datetime.today(),
            ora="12:00",
            tipo="concerto"
        )

    def test_mappa_modena(self):
        resp = self.client.get(reverse('mappa_modena'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mappe/mappa.html')

    def test_register_view_crea_utente(self):
        resp = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password12345',
            'password2': 'password12345'
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)


    def test_elimina_evento_staff(self):
        self.client.login(username='staff', password='pass')
        resp = self.client.post(reverse('elimina_evento', args=[self.evento.id]))
        self.assertRedirects(resp, reverse('lista'))
        self.assertFalse(Evento.objects.filter(id=self.evento.id).exists())

    def test_lista_utenti_superuser(self):
        self.client.login(username='super', password='pass')
        resp = self.client.get(reverse('lista_utenti'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.user.username)

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
