import django_tables2 as tables

from .models import Incasso, Transazione


class ImportoColumn(tables.Column):
    def render_footer(self, bound_column, table):
        total = sum(bound_column.accessor.resolve(row) for row in table.data)
        return total

    def render(self, value):
        return value


class IncassoTable(tables.Table):
    class Meta:
        model = Incasso
        order_by = "ricevuta"
        orderable = True
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "data",
            "importo",
            "ricevuta",
            "canale",
            "committente",
            "versato",
        )

    importo = ImportoColumn(attrs={"tf": {"class": "fw-bold"}})
    data = tables.DateTimeColumn(format="d/m/y")

    ricevuta = tables.Column(linkify=("incasso_detail_view", [tables.A("ricevuta")]))

    _ = tables.TemplateColumn(
        template_code='<a href="{% url \'incasso_edit_view\' record.pk %}" class="btn btn-info">Modifica</a>'
    )
    __ = tables.TemplateColumn(
        template_code='<a href="{% url \'incasso_delete_view\' record.pk %}" class="btn btn-danger">Cancella</a>'
    )

    def value_importo(self, value):
        return float(value)

    def before_render(self, request):
        if request.user.is_staff:
            self.columns.show("_")
            self.columns.show("__")
        else:
            self.columns.hide("_")
            self.columns.hide("__")


class NumeroIncassiColumn(tables.Column):
    def render(self, value):
        return value.count


class TransazioneTable(tables.Table):
    class Meta:
        model = Transazione
        order_by = "data"
        orderable = True
        template_name = "django_tables2/bootstrap.html"
        fields = ("data", "importo", "tipologia", "incassi")

    importo = ImportoColumn(attrs={"tf": {"class": "fw-bold"}})
    data = tables.DateTimeColumn(format="d/m/y")

    incassi = NumeroIncassiColumn(verbose_name="Incassi Collegati")

    ___ = tables.TemplateColumn(
        template_code='<a href="{% url \'transazione_detail_view\' record.pk %}" class="btn btn-success">Dettaglio</a>'
    )
    _ = tables.TemplateColumn(
        template_code='<a href="{% url \'transazione_edit_view\' record.pk %}" class="btn btn-info">Modifica</a>'
    )
    __ = tables.TemplateColumn(
        template_code='<a href="{% url \'transazione_delete_view\' record.pk %}" class="btn btn-danger">Cancella</a>'
    )

    def value_importo(self, value):
        return float(value)

    def before_render(self, request):
        if request.user.is_staff:
            self.columns.show("_")
            self.columns.show("__")
        else:
            self.columns.hide("_")
            self.columns.hide("__")
