from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm
from .models import Evento
from .forms import EventoForm
from django.utils import timezone
from datetime import timedelta
import re
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

def mappa_modena(request):
    eventi = Evento.objects.all()
    context = {
        'eventi': eventi
    }
    return render(request, 'mappe/mappa.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mappa_modena') # Reindirizza alla mappa dopo la registrazione
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form,
        'background': '/media/MoEventsCollage.png'
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('mappa_modena')
        else:
            return render(request, 'login.html', {'error_message': 'Credenziali non valide'})
    return render(request, 'login.html', {
        'background': '/media/MoEventsCollage.png', 'logo_url': '/media/MoEventsLogo.png'
    })

def logout_view(request):
    logout(request)
    return redirect('mappa_modena')

@login_required(login_url='/login/') 
def lista_view(request):
    eventi = Evento.objects.all().order_by('data', 'ora')
    context = {
        'eventi': eventi
    }
    return render(request, 'mappe/lista.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def elimina_evento(request, evento_id):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=evento_id)
        evento.delete()
    return redirect('lista')



@login_required
@user_passes_test(lambda u: u.is_staff)
def modifica_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'mappe/modifica_evento.html', {'form': form, 'evento': evento})

@login_required
def dettaglio_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'mappe/dettaglio_evento.html', {'evento': evento})

@login_required
def lista_view(request):
    eventi = Evento.objects.all()

    query = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "")
    data = request.GET.get("data", "")

    oggi = timezone.now().date()
    ieri = oggi - timedelta(days=1)

    query = request.GET.get("q", "").strip()

    if len(query) > 100:
        query = query[:100]  

    if query:
        eventi = eventi.filter(titolo__icontains=query)

    if tipo:
        eventi = eventi.filter(tipo=tipo)

    if data:
        eventi = eventi.filter(data=data)

    return render(request, "mappe/lista.html", {
        "eventi": eventi,
        "query": query,
        "tipo": tipo,
        "data": data,
    })

@user_passes_test(lambda u: u.is_superuser)
def lista_utenti(request):
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, pk=user_id)

        if action == "make_staff":
            user.is_staff = True
            user.save()
        elif action == "remove_staff":
            user.is_staff = False
            user.save()
        elif action == "make_superuser":
            user.is_superuser = True
            user.save()
        elif action == "remove_superuser":
            user.is_superuser = False
            user.save()
        elif action == "delete":
            user.delete()

        return redirect("lista_utenti")

    utenti = User.objects.all()
    return render(request, "mappe/lista_utenti.html", {"utenti": utenti})

