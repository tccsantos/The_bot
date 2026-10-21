from django import forms
from django.utils import timezone
from .models import Event

today = timezone.localdate()

class PreGameForm(forms.Form):
    padoru = forms.TypedChoiceField(
        choices=[
            ("True", "Sim"),
            ("False", "Não"),
        ],
        coerce=lambda value: value == "True",
        label="Somente temas com Padorus?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    available = forms.TypedChoiceField(
        choices=[
            ("True", "Sim"),
            ("False", "Não"),
        ],
        coerce=lambda value: value == "True",
        label="Somente temas ainda não utilizados?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    event_date = forms.ChoiceField(
        label="Data da partida",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, event_dates=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["event_date"].choices = event_dates or []

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'theme': "Tema",
            'month': "Mês",
            'year': "Ano",
        }
