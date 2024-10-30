from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incasso, Transazione, CassaDelGiorno


@receiver(post_save, sender=Incasso)
def update_cassa_del_giorno_on_incasso(sender, instance, created, **kwargs):
    """
    Aggiorna i campi della CassaDelGiorno quando viene salvato un nuovo Incasso.
    """
    cassa_del_giorno, _ = CassaDelGiorno.objects.get_or_create(data=instance.data)
    cassa_del_giorno.totale_incassi += instance.importo
    cassa_del_giorno.saldo = (
        cassa_del_giorno.totale_incassi - cassa_del_giorno.totale_transazioni
    )
    cassa_del_giorno.save()


@receiver(post_save, sender=Transazione)
def update_cassa_del_giorno_on_transazione(sender, instance, created, **kwargs):
    """
    Aggiorna i campi della CassaDelGiorno quando viene salvata una nuova Transazione.
    """
    cassa_del_giorno, _ = CassaDelGiorno.objects.get_or_create(data=instance.data)
    cassa_del_giorno.totale_transazioni += instance.importo
    cassa_del_giorno.saldo = (
        cassa_del_giorno.totale_transazioni - cassa_del_giorno.totale_incassi
    )
    cassa_del_giorno.save()
