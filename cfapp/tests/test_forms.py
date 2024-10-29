import datetime
from django.test import TestCase
from ..models import Committenti, Canali, TipologiaTransazione, Transazione, Incasso
from ..forms import TransazioneForm, IncassoForm


class TestTransazioneForm(TestCase):
    def setUp(self):
        self.tipologia_transazione1 = TipologiaTransazione.objects.create(
            tipologia_transazione="Transazione 1"
        )
        self.tipologia_transazione2 = TipologiaTransazione.objects.create(
            tipologia_transazione="Transazione 2"
        )
        self.transazione1 = Transazione.objects.create(
            importo=50, tipologia=self.tipologia_transazione1, data="2023-01-15"
        )
        self.transazione2 = Transazione.objects.create(
            importo=75, tipologia=self.tipologia_transazione2, data="2023-02-15"
        )
        self.committente1 = Committenti.objects.create(
            codice="ABC", committente="Committente 1"
        )
        self.committente2 = Committenti.objects.create(
            codice="DEF", committente="Committente 2"
        )
        self.canale1 = Canali.objects.create(canale="Canale 1", flag_auto_versato=False)
        self.canale2 = Canali.objects.create(canale="Canale 2", flag_auto_versato=True)
        self.incasso1 = Incasso.objects.create(
            importo=100,
            data="2023-01-01",
            ricevuta="123456",
            canale=self.canale1,
            committente=self.committente1,
        )
        self.incasso2 = Incasso.objects.create(
            importo=200,
            data="2023-02-01",
            ricevuta="789012",
            canale=self.canale2,
            committente=self.committente2,
        )

    def test_transazione_form_valid(self):
        data = {
            "importo": 80,
            "tipologia": self.tipologia_transazione1.id,
            "data": "2023-03-01",
            "incassi": [self.incasso1.id, self.incasso2.id],
        }
        form = TransazioneForm(data=data)
        self.assertTrue(form.is_valid())

        transazione = form.save()
        self.assertEqual(transazione.importo, 80)
        self.assertEqual(transazione.tipologia, self.tipologia_transazione1)
        self.assertEqual(transazione.data, datetime.date(2023, 3, 1))
        self.assertCountEqual(transazione.incassi.all(), [self.incasso1, self.incasso2])

    def test_transazione_form_invalid(self):
        data = {
            "importo": -50,
            "tipologia": self.tipologia_transazione1.id,
            "data": "2023-03-41",
            "incassi": [self.incasso1.id, self.incasso2.id],
        }
        form = TransazioneForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("data", form.errors)


class TestIncassoForm(TestCase):
    def setUp(self):
        self.tipologia_transazione1 = TipologiaTransazione.objects.create(
            tipologia_transazione="Transazione 1"
        )
        self.tipologia_transazione2 = TipologiaTransazione.objects.create(
            tipologia_transazione="Transazione 2"
        )
        self.transazione1 = Transazione.objects.create(
            importo=50, tipologia=self.tipologia_transazione1, data="2023-01-15"
        )
        self.transazione2 = Transazione.objects.create(
            importo=75, tipologia=self.tipologia_transazione2, data="2023-02-15"
        )
        self.committente1 = Committenti.objects.create(
            codice="ABC", committente="Committente 1"
        )
        self.committente2 = Committenti.objects.create(
            codice="DEF", committente="Committente 2"
        )
        self.canale1 = Canali.objects.create(canale="Canale 1", flag_auto_versato=False)
        self.canale2 = Canali.objects.create(canale="Canale 2", flag_auto_versato=True)

    def test_incasso_form_valid(self):
        data = {
            "importo": 120,
            "data": "2023-03-01",
            "ricevuta": "123456",
            "canale": self.canale1.id,
            "committente": self.committente1.id,
            "versato": True,
            "transazioni": [self.transazione1.id, self.transazione2.id],
        }
        form = IncassoForm(data=data)
        self.assertTrue(form.is_valid())

        incasso = form.save()
        self.assertEqual(incasso.importo, 120)
        self.assertEqual(incasso.data, datetime.date(2023, 3, 1))
        self.assertEqual(incasso.ricevuta, "123456")
        self.assertEqual(incasso.canale, self.canale1)
        self.assertEqual(incasso.committente, self.committente1)
        self.assertTrue(incasso.versato)
        self.assertCountEqual(
            incasso.transazioni.all(), [self.transazione1, self.transazione2]
        )

    def test_incasso_form_invalid(self):
        data = {
            "importo": -120,
            "data": "2023-03-41",
            "ricevuta": "123",
            "canale": self.canale1.id,
            "committente": self.committente1.id,
            "versato": True,
            "transazioni": [self.transazione1.id, self.transazione2.id],
        }
        form = IncassoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("data", form.errors)
        self.assertIn("ricevuta", form.errors)
