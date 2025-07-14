from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Evento
from datetime import datetime

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

    def test_lista_view_richiede_login(self):
        resp = self.client.get(reverse('lista'))
        self.assertRedirects(
            resp,
            '/login/?next=' + reverse('lista')
        )

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
