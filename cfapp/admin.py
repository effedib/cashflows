from django.contrib import admin

from .models import Incasso, Transazione, Committenti, Canali, TipologiaTransazione


class IncassoInline(admin.TabularInline):
    model = Incasso
    extra = 1 


@admin.register(TipologiaTransazione)
class TipologiaTransazioneAdmin(admin.ModelAdmin):
    list_display = ("tipologia_transazione",)
    search_fields = ("tipologia_transazione",)


@admin.register(Transazione)
class TransazioneAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipologia', 'importo', 'numero_incassi')
    list_filter = ('data',)
    search_fields = ('tipologia',)
    inlines = [IncassoInline]
    
    def numero_incassi(self, obj):
        return obj.transazioni.count()
    numero_incassi.short_description = 'Numero di incassi'

# @admin.register(Incasso)
# class IncassoAdmin(admin.ModelAdmin):
#     list_display = ('transazione', 'importo', 'metodo_pagamento')
#     list_filter = ('metodo_pagamento', 'transazione__data')
#     search_fields = ('note', 'transazione__descrizione')

admin.site.register(Incasso)
admin.site.register(Committenti)
admin.site.register(Canali)
