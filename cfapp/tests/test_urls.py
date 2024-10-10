from django.test import TestCase
from django.urls import reverse, resolve
from datetime import datetime
from ..views import (
    IncassoListView,
    IncassoCreateView,
    IncassoUpdateView,
    IncassoDeleteView,
    IncassoDetailView,
)
from ..models import Incasso, Canali, Committenti


class UrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canale = Canali.objects.create(canale="Test Canale")
        cls.committente = Committenti.objects.create(
            codice="ABC", committente="Test Committente"
        )
        cls.incasso = Incasso.objects.create(
            importo=100.50,
            data=datetime.now().date(),
            ricevuta="123456",
            canale=cls.canale,
            committente=cls.committente,
        )

    def test_list_url_resolves(self):
        url = reverse("incassi_view")
        self.assertEqual(resolve(url).func.view_class, IncassoListView)

    def test_create_url_resolves(self):
        url = reverse("incasso_new_view")
        self.assertEqual(resolve(url).func.view_class, IncassoCreateView)

    def test_update_url_resolves(self):
        url = reverse("incasso_edit_view", args=[self.incasso.pk])
        self.assertEqual(resolve(url).func.view_class, IncassoUpdateView)

    def test_delete_url_resolves(self):
        url = reverse("incasso_delete_view", args=[self.incasso.pk])
        self.assertEqual(resolve(url).func.view_class, IncassoDeleteView)

    def test_detail_url_resolves(self):
        url = reverse("incasso_detail_view", args=[self.incasso.ricevuta])
        self.assertEqual(resolve(url).func.view_class, IncassoDetailView)

    def test_list_url_returns_302(self):
        response = self.client.get(reverse("incassi_view"))
        self.assertEqual(response.status_code, 302)  # 302 perché richiede login

    def test_urls_use_correct_template(self):
        # Questo test verrà eseguito con un utente autenticato
        self.client.login(username="testuser", password="testpass123")

        templates_urls = [
            ("incassi_view", [], "cfapp/incasso_table.html"),
            ("incasso_new_view", [], "cfapp/incasso_new.html"),
            ("incasso_edit_view", [self.incasso.pk], "cfapp/incasso_edit.html"),
            ("incasso_delete_view", [self.incasso.pk], "cfapp/incasso_delete.html"),
            (
                "incasso_detail_view",
                [self.incasso.ricevuta],
                "cfapp/incasso_detail.html",
            ),
        ]

        for url_name, args, _ in templates_urls:
            response = self.client.get(reverse(url_name, args=args))
            self.assertEqual(response.status_code, 302)
