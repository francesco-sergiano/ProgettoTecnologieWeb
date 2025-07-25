# urls.py app
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Mappa come pagina di default (accessibile a tutti)
    path('', views.mappa_modena, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mappa/', views.mappa_modena, name='mappa_modena'),
    path('lista/', views.lista_view, name='lista'),
    path('salva/<int:evento_id>/', views.salva_evento, name='salva_evento'),
    path('rimuovi/<int:evento_id>/', views.rimuovi_evento, name='rimuovi_evento'),
    path('elimina/<int:evento_id>/', views.elimina_evento, name='elimina_evento'),
    path('modifica/<int:evento_id>/', views.modifica_evento, name='modifica_evento'),
    path('evento/<int:evento_id>/', views.dettaglio_evento, name='dettaglio_evento'),
    path("nuovo_evento/", views.nuovo_evento, name="nuovo_evento"),
    path('utenti/', views.lista_utenti, name='lista_utenti'),
    path('statistiche/', views.statistiche, name='statistiche'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)