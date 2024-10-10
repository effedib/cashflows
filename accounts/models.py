from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Office(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")


class CustomUser(AbstractUser):
    team = models.ForeignKey(
        Office, on_delete=models.PROTECT, null=True, blank=True, related_name="users"
    )
