from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Evento, Visita, EventoSalvato
from datetime import date, time


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.evento = Evento.objects.create(
            titolo='Test Evento',
            descrizione='Descrizione evento',
            luogo='Modena',
            data=date.today(),
            ora=time(18, 0),
            tipo='EVENTO',
            latitudine=44.0,
            longitudine=10.9,
        )

    def test_evento_str(self):
        """Verifica la stringa restituita dal modello Evento"""
        self.assertIn(self.evento.titolo, str(self.evento))

    def test_visita_str(self):
        """Verifica la stringa restituita dal modello Visita"""
        visita = Visita.objects.create(user=self.user)
        self.assertIn(self.user.username, str(visita))

    def test_evento_salvato_unique(self):
        """Verifica che non si possano salvare due volte lo stesso evento per lo stesso utente"""
        EventoSalvato.objects.create(user=self.user, evento=self.evento)
        with self.assertRaises(Exception):  # Violazione unique_together
            EventoSalvato.objects.create(user=self.user, evento=self.evento)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff = User.objects.create_user(username='staffuser', password='testpass', is_staff=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='testpass')
        self.evento = Evento.objects.create(
            titolo='Test Evento',
            descrizione='Descrizione evento',
            luogo='Modena',
            data=date.today(),
            ora=time(18, 0),
            tipo='EVENTO',
            latitudine=44.0,
            longitudine=10.9,
        )

    def test_mappa_modena_view(self):
        """La vista mappa_modena risponde correttamente"""
        resp = self.client.get(reverse('mappa_modena'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mappe/mappa.html')

    def test_register_view_get(self):
        """La vista register restituisce la pagina di registrazione"""
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view_get(self):
        """La vista login restituisce la pagina di login"""
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_view(self):
        """Il logout redireziona alla mappa"""
        self.client.login(username='testuser', password='testpass')
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, reverse('mappa_modena'))

    def test_lista_view(self):
        """La vista lista restituisce la lista eventi"""
        resp = self.client.get(reverse('lista'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mappe/lista.html')

    def test_dettaglio_evento(self):
        """La vista dettaglio_evento restituisce i dettagli di un evento"""
        resp = self.client.get(reverse('dettaglio_evento', args=[self.evento.id]))
        self.assertEqual(resp.status_code, 200)

    def test_salva_e_rimuovi_evento(self):
        """Un utente autenticato può salvare e rimuovere un evento"""
        self.client.login(username='testuser', password='testpass')
        salva_url = reverse('salva_evento', args=[self.evento.id])
        rimuovi_url = reverse('rimuovi_evento', args=[self.evento.id])
        resp = self.client.post(salva_url)
        self.assertEqual(resp.status_code, 302)  # redirect dopo salvataggio
        resp = self.client.post(rimuovi_url)
        self.assertEqual(resp.status_code, 302)  # redirect dopo rimozione


class UrlsTestCase(TestCase):
    def test_urls_resolve(self):
        """Verifica che tutte le URL siano configurate e risolvibili"""
        urls = [
            ('mappa_modena', []),
            ('register', []),
            ('login', []),
            ('logout', []),
            ('lista', []),
            ('nuovo_evento', []),
            ('lista_utenti', []),
            ('statistiche', []),
        ]
        for name, args in urls:
            url = reverse(name, args=args)
            resolved = resolve(url)
            self.assertIsNotNone(resolved.func)

        # URL che richiedono un evento_id
        evento_id = 1
        for name in ['salva_evento', 'rimuovi_evento', 'elimina_evento', 'modifica_evento', 'dettaglio_evento']:
            url = reverse(name, args=[evento_id])
            resolved = resolve(url)
            self.assertIsNotNone(resolved.func)
