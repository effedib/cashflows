import django_tables2 as tables
from .models import Incasso

class IncassoTable(tables.Table):
    class Meta:
        model = Incasso
        template_name = "django_tables2/bootstrap.html"
        fields = ("data", "importo", "ricevuta", "canale",
                  "committente", "versato", "transazione")

