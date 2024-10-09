from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime
from ..models import Incasso, Canali, Committenti

User = get_user_model()

class IncassoViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.staff_user = User.objects.create_user(
            username="staffuser", password="staffpass123", is_staff=True
        )
        cls.canale = Canali.objects.create(canale="Test Canale")
        cls.committente = Committenti.objects.create(codice="ABC", committente="Test Committente")
        cls.incasso = Incasso.objects.create(
            importo=100.50,
            data=datetime.now().date(),
            ricevuta="123456",
            canale=cls.canale,
            committente=cls.committente
        )

    def setUp(self):
        self.client = Client()

    def test_list_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('incassi_view'))
        self.assertRedirects(response, '/accounts/login/?next=/incassi/')

    def test_list_view_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('incassi_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cfapp/incasso_table.html')

    def test_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('incasso_new_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cfapp/incasso_new.html')

    def test_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('incasso_edit_view', args=[self.incasso.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cfapp/incasso_edit.html')

    def test_delete_view_staff_only(self):
        # Test with regular user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('incasso_delete_view', args=[self.incasso.pk]))
        self.assertRedirects(response, reverse('incassi_view'))

        # Test with staff user
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('incasso_delete_view', args=[self.incasso.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cfapp/incasso_delete.html')

    def test_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('incasso_detail_view', args=[self.incasso.ricevuta]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cfapp/incasso_detail.html')
        self.assertEqual(response.context['object'], self.incasso)