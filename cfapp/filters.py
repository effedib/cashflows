import django_filters
from .models import Incasso, Transazione


class IncassoFilter(django_filters.FilterSet):
    class Meta:
        model = Incasso
        fields = [
            "data",
            "importo",
            "ricevuta",
            "canale",
            "committente",
            "versato",
        ]


class TransazioneFilter(django_filters.FilterSet):
    class Meta:
        model = Transazione
        fields = [
            "data",
            "importo",
            "tipologia",
        ]