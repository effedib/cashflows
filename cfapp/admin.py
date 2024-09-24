from django.contrib import admin

from .models import Incasso, Transazione

admin.site.register(Incasso)
admin.site.register(Transazione)
