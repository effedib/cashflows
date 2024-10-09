from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from datetime import datetime
from ..models import Incasso, Canali, Committenti
from ..tables import IncassoTable

User = get_user_model()

class IncassoTableTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123", is_staff=False)
        cls.staff_user = User.objects.create_user(
            username="staffuser", password="staffpass123", is_staff=True
        )
        cls.canale = Canali.objects.create(canale="Test Canale")
        cls.committente = Committenti.objects.create(codice="ABC", committente="Test Committente")
        cls.incasso = Incasso.objects.create(
            importo=100.50,
            data=datetime(2024, 1, 1).date(),
            ricevuta="123456",
            canale=cls.canale,
            committente=cls.committente
        )
        cls.factory = RequestFactory()

    def test_table_renders(self):
        request = self.factory.get('/')
        request.user = self.user
        table = IncassoTable(Incasso.objects.all())
        table_html = table.as_html(request)
        self.assertIn(self.incasso.ricevuta, table_html)

    def test_importo_column_footer(self):
        Incasso.objects.create(
            importo=200.75,
            data=datetime(2024, 1, 2).date(),
            ricevuta="654321"
        )
        table = IncassoTable(Incasso.objects.all())
        self.assertEqual(float(table.columns['importo'].footer), 301.25)

    def test_staff_buttons_visibility(self):
        # Test for regular user
        request = self.factory.get('/')
        request.user = self.user
        table = IncassoTable(Incasso.objects.all())
        table.before_render(request)

        # Verifica che le colonne siano nascoste per gli utenti normali
        self.assertFalse(table.columns['_'].visible)
        self.assertFalse(table.columns['__'].visible)

        # Test for staff user
        request.user = self.staff_user
        table = IncassoTable(Incasso.objects.all())
        table.before_render(request)

        # Verifica che le colonne siano visibili per gli utenti staff
        self.assertTrue(table.columns['_'].visible)
        self.assertTrue(table.columns['__'].visible)

    def test_link_in_ricevuta_column(self):
        request = self.factory.get('/')
        request.user = self.user
        table = IncassoTable(Incasso.objects.all())
        table_html = table.as_html(request)
        expected_url = f'/incassi/{self.incasso.ricevuta}/'
        self.assertIn(expected_url, table_html)

    def test_data_format(self):
        request = self.factory.get('/')
        request.user = self.user
        table = IncassoTable(Incasso.objects.all())
        table_html = table.as_html(request)
        formatted_date = self.incasso.data.strftime("%d/%m/%y")
        self.assertIn(formatted_date, table_html)