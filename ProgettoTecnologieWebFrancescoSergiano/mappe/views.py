from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .forms import RegisterForm, EventoForm
from .models import Evento, Visita, EventoSalvato
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from django.core.paginator import Paginator



def mappa_modena(request):
    eventi = Evento.objects.all()
    if request.user.is_authenticated:
        Visita.objects.create(user=request.user)
    else:
        Visita.objects.create()

    context = {
        'eventi': eventi,
        'logo_url': '/media/MoEventsLogo.png',
        'creazione': request.GET.get('creazione') == '1'
    }
    return render(request, 'mappe/mappa.html', context)



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mappa_modena')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {
        'form': form,
        'background': '/media/MoEventsCollage.png',
        'logo_url': '/media/MoEventsLogo.png'
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
        'background': '/media/MoEventsCollage.png',
        'logo_url': '/media/MoEventsLogo.png'
    })


def logout_view(request):
    logout(request)
    return redirect('mappa_modena')



def lista_view(request):
    eventi = Evento.objects.all()

    query = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "")
    data = request.GET.get("data", "")
    salvati = request.GET.get("salvati", "")

    if query:
        eventi = eventi.filter(titolo__icontains=query)

    if tipo:
        eventi = eventi.filter(tipo=tipo)

    if data:
        eventi = eventi.filter(data=data)

    if request.user.is_authenticated:
        salvati_ids = set(EventoSalvato.objects.filter(user=request.user).values_list('evento_id', flat=True))
    else:
        salvati_ids = set()

    if salvati == "1":  # Solo salvati
        eventi = eventi.filter(id__in=salvati_ids)
    elif salvati == "0":  # Non salvati
        eventi = eventi.exclude(id__in=salvati_ids)


    paginator = Paginator(eventi, 6)  # 6 eventi per pagina
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "mappe/lista.html", {
        "eventi": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "tipo": tipo,
        "data": data,
        "salvati": salvati,
        "salvati_ids": list(salvati_ids),
    })

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



def dettaglio_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    # 📈 Registra la visita
    if request.user.is_authenticated:
        Visita.objects.create(user=request.user, evento=evento)
    else:
        Visita.objects.create(evento=evento)

    return render(request, 'mappe/dettaglio_evento.html', {'evento': evento})


@user_passes_test(lambda u: u.is_superuser)
@login_required
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def nuovo_evento(request):
    lat = request.GET.get('latitudine')
    lng = request.GET.get('longitudine')

    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("mappa_modena")
    else:
        form = EventoForm(initial={
            'latitudine': lat,
            'longitudine': lng
        })

    return render(request, "mappe/nuovo_evento.html", {
        "form": form,
        "today": date.today().isoformat()
    })


@staff_member_required
def statistiche(request):
    eventi = Evento.objects.all()
    totale = eventi.count()
    percentuali = eventi.values('tipo').annotate(count=Count('id'))

    stats_eventi = {
        e['tipo']: round(e['count'] / totale * 100, 1) if totale > 0 else 0
        for e in percentuali
    }

    oggi = timezone.now() - timedelta(days=1)
    mese = timezone.now() - timedelta(days=30)
    anno = timezone.now() - timedelta(days=365)

    visite_oggi = Visita.objects.filter(timestamp__gte=oggi).count()
    visite_mese = Visita.objects.filter(timestamp__gte=mese).count()
    visite_anno = Visita.objects.filter(timestamp__gte=anno).count()

    # 👇 Eventi più e meno cliccati
    eventi_visite = Evento.objects.annotate(visite_count=Count('visita')).order_by('-visite_count')

    evento_piu_cliccato = eventi_visite.first()
    evento_meno_cliccato = eventi_visite.last()

    context = {
        'stats_eventi': stats_eventi,
        'visite_oggi': visite_oggi,
        'visite_mese': visite_mese,
        'visite_anno': visite_anno,
        'evento_piu_cliccato': evento_piu_cliccato,
        'evento_meno_cliccato': evento_meno_cliccato,
    }

    return render(request, 'mappe/statistiche.html', context)

@login_required
def salva_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    EventoSalvato.objects.get_or_create(user=request.user, evento=evento)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('lista')))

@login_required
def rimuovi_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    EventoSalvato.objects.filter(user=request.user, evento=evento).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('lista')))