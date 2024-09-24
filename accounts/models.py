from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class Offices(models.TextChoices):
        BACKOFFICE = "BO", _("Back Office")
        FRONTOFFICE = "FO", _("Front Office")
        PIANIFICAZIONESTRATEGICA = "PS", _("Pianificazione Strategica")
        MANAGEMENT = "MG", _("Management")

    team = models.CharField(max_length=50, choices=Offices, default=Offices.BACKOFFICE)
    