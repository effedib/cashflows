from django.contrib import admin

from .models import Incasso, Transazione, Committenti, Canali, TipologiaTransazione


class IncassoInline(admin.TabularInline):
    model = Incasso.transazioni.through
    extra = 0


@admin.register(TipologiaTransazione)
class TipologiaTransazioneAdmin(admin.ModelAdmin):
    list_display = ("nome_transazione",)
    search_fields = ("nome_transazione","tipo_transazione")
    fields = ("nome_transazione","tipo_transazione")


@admin.register(Transazione)
class TransazioneAdmin(admin.ModelAdmin):
    list_display = ("data", "tipologia", "importo", "numero_incassi")
    list_filter = ("data",)
    search_fields = ("tipologia",)
    inlines = [IncassoInline]

    def numero_incassi(self, obj):
        return obj.incassi.count()

    numero_incassi.short_description = "Numero di incassi"


@admin.register(Incasso)
class IncassoAdmin(admin.ModelAdmin):
    inlines = [IncassoInline]
    exclude = ["transazione"]
    list_display = (
        "importo",
        "data",
        "ricevuta",
        "canale",
        "committente",
        "versato",
    )
    list_filter = (
        "importo",
        "data",
        "ricevuta",
        "canale",
        "committente",
        "versato",
    )
    search_fields = (
        "importo",
        "data",
        "ricevuta",
        "canale__canale",
        "committente__codice",
        "committente__committente",
        "transazione__tipologia__nome_transazione",
    )


admin.site.register(Committenti)
admin.site.register(Canali)
