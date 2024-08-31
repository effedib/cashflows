from django.db import models
from django.utils.translation import gettext_lazy as _


class Transazioni(models.Model):
    importo = models.FloatField(default=0)
    tipologia = models.CharField(max_length=200)
    data = models.DateTimeField("data operazione")
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class Incassi(models.Model):

    class Canali(models.TextChoices):
        CONTANTI = 'CO', _('Contanti')
        ASSEGNOCIRCOLARE = 'AC', _('Assegno Circolare')
        VERSAMENTOCARTA = 'CA', _('Versamento Carta Esattori')
        POS = 'POS', _('Incasso tramite POS')


    importo = models.FloatField(default=0)
    data = models.DateTimeField("data ricevuta")
    ricevuta = models.CharField(max_length=6)
    canale = models.CharField(choices=Canali.choices, max_length=200)
    committente = models.CharField(max_length=200)
    versato = models.BooleanField(default=False)
    transazione = models.ForeignKey(Transazioni, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"{self.ricevuta}"
