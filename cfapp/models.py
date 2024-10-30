from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Committenti(models.Model):
    class Meta:
        verbose_name = "Committente"
        verbose_name_plural = "Committenti"

    codice = models.CharField(
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(3)],
        max_length=3,
    )
    committente = models.CharField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        self.codice = self.codice.upper()
        self.committente = self.committente.upper()

        super(Committenti, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.committente}"


class Canali(models.Model):
    class Meta:
        verbose_name = "Canale"
        verbose_name_plural = "Canali"

    canale = models.CharField(unique=True, max_length=100)
    flag_auto_versato = models.BooleanField(
        "Il canale comprende il versamento da parte dell'esattore", default=False
    )

    def save(self, *args, **kwargs):
        self.canale = self.canale.capitalize()

        super(Canali, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.canale}"


class TipologiaTransazione(models.Model):
    class Meta:
        verbose_name = "Tipologia transazione"
        verbose_name_plural = "Tipologie transazioni"

    tipologia_transazione = models.CharField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        self.tipologia_transazione = self.tipologia_transazione.capitalize()

        super(TipologiaTransazione, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipologia_transazione}"


class Transazione(models.Model):
    class Meta:
        verbose_name = "Transazione"
        verbose_name_plural = "Transazioni"

    importo = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    tipologia = models.ForeignKey(
        TipologiaTransazione,
        on_delete=models.PROTECT,
        blank=True,
        related_name="tipologia",
    )
    data = models.DateField("data operazione")
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self) -> str:
        data = self.data.strftime("%d-%m-%Y")
        return f"{self.tipologia} / €{self.importo:.2f} / {data}"


class Incasso(models.Model):
    class Meta:
        verbose_name = "Incasso"
        verbose_name_plural = "Incassi"

    importo = models.DecimalField(decimal_places=2, max_digits=8)
    data = models.DateField("data ricevuta")
    ricevuta = models.CharField(
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
        max_length=6,
    )
    canale = models.ForeignKey(Canali, on_delete=models.PROTECT, blank=True, null=True)
    committente = models.ForeignKey(
        Committenti, on_delete=models.PROTECT, blank=True, null=True
    )
    versato = models.BooleanField(default=False, blank=True, null=True)
    transazioni = models.ManyToManyField(
        Transazione, blank=True, related_name="incassi"
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"ricevuta: {self.ricevuta} - importo: {self.importo:.2f}"

    def get_absolute_url(self):
        return reverse("incasso_detail_view", kwargs={"pk": self.ricevuta})
