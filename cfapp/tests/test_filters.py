from django.test import TestCase
from datetime import datetime
from ..models import Incasso, Canali, Committenti
from ..filters import IncassoFilter

class IncassoFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canale = Canali.objects.create(canale="Test Canale")
        cls.committente = Committenti.objects.create(codice="ABC", committente="Test Committente")
        cls.incasso1 = Incasso.objects.create(
            importo=100.50,
            data=datetime(2024, 1, 1).date(),
            ricevuta="123456",
            canale=cls.canale,
            committente=cls.committente,
            versato=True
        )
        cls.incasso2 = Incasso.objects.create(
            importo=200.75,
            data=datetime(2024, 1, 2).date(),
            ricevuta="654321",
            canale=cls.canale,
            committente=cls.committente,
            versato=False
        )

    def test_filter_by_importo(self):
        f = IncassoFilter({'importo': 100.50}, queryset=Incasso.objects.all())
        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.incasso1)

    def test_filter_by_ricevuta(self):
        f = IncassoFilter({'ricevuta': '123456'}, queryset=Incasso.objects.all())
        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.incasso1)

    def test_filter_by_canale(self):
        f = IncassoFilter({'canale': self.canale.id}, queryset=Incasso.objects.all())
        self.assertEqual(len(f.qs), 2)

    def test_filter_by_committente(self):
        f = IncassoFilter({'committente': self.committente.id}, queryset=Incasso.objects.all())
        self.assertEqual(len(f.qs), 2)

    def test_filter_by_versato(self):
        f = IncassoFilter({'versato': True}, queryset=Incasso.objects.all())
        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.incasso1)