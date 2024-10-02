from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Transazione(models.Model):
    class Meta:
        verbose_name = "Transazione"
        verbose_name_plural = "Transazioni"

    importo = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    tipologia = models.CharField(max_length=200)
    data = models.DateTimeField("data operazione")
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}: importo = {self.importo} - data = {self.data.strftime('%d-%m-%Y')} - tipologia = {self.tipologia}"


class Incasso(models.Model):
    class Meta:
        verbose_name = "Incasso"
        verbose_name_plural = "Incassi"

    class Canali(models.TextChoices):
        CONTANTI = "CO", _("Contanti")
        ASSEGNOCIRCOLARE = "AC", _("Assegno Circolare")
        VERSAMENTOCARTA = "CA", _("Versamento Carta Esattori")
        POS = "POS", _("Incasso tramite POS")

    class Committenti(models.TextChoices):
        COMPASS = "COM", _("Compass Banca S.p.A.")
        AGOS = "AGO", _("Agos Ducato S.p.A.")
        FIDITALIA = "FID", _("Fiditalia S.p.A.")
        COFIDIS = "CFD", _("Cofidis S.p.A.")

    importo = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    data = models.DateTimeField("data ricevuta")
    ricevuta = models.CharField(
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
        max_length=6,
    )
    canale = models.CharField(choices=Canali.choices, max_length=200)
    committente = models.CharField(choices=Committenti.choices, max_length=200)
    versato = models.BooleanField(default=False)
    transazione = models.ForeignKey(
        Transazione, on_delete=models.PROTECT, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    

    def __str__(self):
        return f"ricevuta: {self.ricevuta} - importo: {self.importo:.2f}"

    def get_absolute_url(self):
        return reverse("incasso_detail_view", kwargs={"pk": self.ricevuta})
