# urls.py della tua app
from django.urls import path
from . import views # Importa tutto da views

urlpatterns = [
    # Mappa come pagina di default (accessibile a tutti)
    path('', views.mappa_modena, name='home'), # Cambiato da login_view a mappa_modena
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mappa/', views.mappa_modena, name='mappa_modena'), # Può rimanere o essere eliminato se la home è sufficiente
    path('lista/', views.lista_view, name='lista'),
    path('elimina/<int:evento_id>/', views.elimina_evento, name='elimina_evento'),
]