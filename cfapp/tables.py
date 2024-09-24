import django_tables2 as tables
from .models import Incasso

    
class ImportoColumn(tables.Column):
    def render(self, value):
        return f"{value:.2f}"
    

class IncassoTable(tables.Table):
    class Meta:
        model = Incasso
        order_by = "ricevuta"
        orderable = True
        template_name = "django_tables2/bootstrap.html"
        fields = ("data", "importo", "ricevuta", "canale",
                  "committente", "versato", "transazione")
    
    importo = ImportoColumn()
    data = tables.DateTimeColumn(format='d/m/y')

    ricevuta = tables.Column(linkify=('incasso_detail_view', [tables.A('ricevuta')]))
