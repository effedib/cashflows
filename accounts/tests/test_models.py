from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Office


class OfficeModelTests(TestCase):
    def test_office_creation(self):
        office = Office.objects.create(name="Test Office")
        self.assertEqual(str(office), "Test Office")
        self.assertEqual(office.name, "Test Office")


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.office = Office.objects.create(name="Test Office")
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            team=self.office,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.team, self.office)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "testuser")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superadmin",
            email="superadmin@example.com",
            password="testpass123",
            team=self.office,
        )
        self.assertEqual(admin_user.username, "superadmin")
        self.assertEqual(admin_user.email, "superadmin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.team, self.office)
