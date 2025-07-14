from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
.
from .models import Evento

admin.site.register(Evento)
# Gruppo per utenti normali
user_group, created = Group.objects.get_or_create(name='User')
