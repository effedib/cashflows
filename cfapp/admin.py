from django.contrib import admin

from .models import Incasso, Transazione, Committenti, Canali

admin.site.register(Incasso)
admin.site.register(Transazione)
admin.site.register(Committenti)
admin.site.register(Canali)
