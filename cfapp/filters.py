import django_filters
from .models import Incasso

class IncassoFilter(django_filters.FilterSet):
    class Meta:
        model = Incasso
        fields = ["data", "importo", "ricevuta", "canale",
                  "committente", "versato", "transazione"]
