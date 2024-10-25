from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime
from ..models import Committenti, Canali, Transazione, Incasso, TipologiaTransazione


class CommittentiTest(TestCase):
    def test_create_committente(self):
        committente = Committenti.objects.create(
            codice="abc", committente="Test Committente"
        )
        self.assertEqual(committente.codice, "ABC")
        self.assertEqual(committente.committente, "TEST COMMITTENTE")

    def test_invalid_codice_length(self):
        with self.assertRaises(ValidationError):
            committente = Committenti(codice="abcd", committente="Test")
            committente.full_clean()

    def test_unique_codice(self):
        Committenti.objects.create(codice="abc", committente="Test 1")
        with self.assertRaises(IntegrityError):
            Committenti.objects.create(codice="abc", committente="Test 2")


class CanaliTest(TestCase):
    def test_create_canale(self):
        canale = Canali.objects.create(canale="test canale", flag_auto_versato=True)
        self.assertEqual(canale.canale, "Test canale")
        self.assertTrue(canale.flag_auto_versato)

    def test_unique_canale(self):
        Canali.objects.create(canale="Test Canale")
        with self.assertRaises(IntegrityError):
            Canali.objects.create(canale="Test Canale")


class TransazioneTest(TestCase):
    def setUp(self):
        self.tipo_transazione = TipologiaTransazione.objects.create(
            tipologia_transazione="Test"
        )

    def test_create_transazione(self):
        transazione = Transazione.objects.create(
            importo=100.50, tipologia=self.tipo_transazione, data=datetime.now()
        )
        self.assertEqual(float(transazione.importo), 100.50)
        self.assertEqual(str(transazione.tipologia), "Test")

    def test_str_representation(self):
        transazione = Transazione.objects.create(
            importo=100.50,
            tipologia=self.tipo_transazione,
            data=datetime(2024, 1, 1, 12, 0),
        )
        expected_str = "Test / €100.50 / 01-01-2024"
        self.assertEqual(str(transazione), expected_str)


class IncassoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canale = Canali.objects.create(canale="Test Canale")
        cls.committente = Committenti.objects.create(
            codice="ABC", committente="Test Committente"
        )
        cls.transazione = Transazione.objects.create(
            importo=100.50,
            data=datetime.now(),
            tipologia=TipologiaTransazione.objects.create(tipologia_transazione="Test"),
        )

    def test_create_incasso(self):
        incasso = Incasso.objects.create(
            importo=100.50,
            data=datetime.now().date(),
            ricevuta="123456",
            canale=self.canale,
            committente=self.committente,
            # transazione=self.transazione,
            versato=True,
        )
        incasso.transazione.set((self.transazione,))
        self.assertEqual(float(incasso.importo), 100.50)
        self.assertEqual(incasso.ricevuta, "123456")
        self.assertTrue(incasso.versato)

    def test_invalid_ricevuta_length(self):
        with self.assertRaises(ValidationError):
            incasso = Incasso(
                importo=100.50,
                data=datetime.now().date(),
                ricevuta="12345",  # Too short
                canale=self.canale,
                committente=self.committente,
            )
            incasso.full_clean()

    def test_str_representation(self):
        incasso = Incasso.objects.create(
            importo=100.50, data=datetime.now().date(), ricevuta="123456"
        )
        expected_str = "ricevuta: 123456 - importo: 100.50"
        self.assertEqual(str(incasso), expected_str)

    def test_get_absolute_url(self):
        incasso = Incasso.objects.create(
            importo=100.50, data=datetime.now().date(), ricevuta="123456"
        )
        self.assertEqual(
            incasso.get_absolute_url(), f"/cfapp/incassi/{incasso.ricevuta}/"
        )
