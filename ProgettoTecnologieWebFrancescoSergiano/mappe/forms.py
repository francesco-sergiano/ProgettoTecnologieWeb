from django import forms
from .models import Evento
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'

        def clean_data(self):
            data = self.cleaned_data['data']
            if data < date.today():
                raise forms.ValidationError("La data non può essere nel passato.")
            return data


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titolo',
            'descrizione',
            'luogo',
            'data',
            'ora',
            'tipo',
            'latitudine',
            'longitudine',
            'immagine',
        ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'ora': forms.TimeInput(attrs={'type': 'time'}),
            'descrizione': forms.Textarea(attrs={'rows': 3}),
        }


    def clean_latitudine(self):
        lat = self.cleaned_data.get('latitudine')
        if lat < -90 or lat > 90:
            raise forms.ValidationError("La latitudine deve essere compresa tra -90 e 90 gradi.")
        return lat

    def clean_longitudine(self):
        lon = self.cleaned_data.get('longitudine')
        if lon < -180 or lon > 180:
            raise forms.ValidationError("La longitudine deve essere compresa tra -180 e 180 gradi.")
        return lon
