from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class CustomUserCreationFormTest(TestCase):
    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected_fields = ["username", "password1", "password2", "team"]
        actual_fields = list(form.fields)
        for field in expected_fields:
            self.assertIn(field, actual_fields)

    def test_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "team": "BO",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            "username": "",  # username vuoto non valido
            "password1": "testpass123",
            "password2": "differentpass",  # password non corrispondenti
            "team": "INVALID",  # team non valido
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class CustomUserChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="existinguser", password="testpass123", team="BO"
        )

    def test_form_has_fields(self):
        form = CustomUserChangeForm(instance=self.user)
        expected_fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "team",
            "password",
        ]
        actual_fields = list(form.fields)
        for field in expected_fields:
            self.assertIn(field, actual_fields)

    def test_form_valid_data(self):
        form = CustomUserChangeForm(instance=self.user)
        initial_data = form.initial.copy()
        form_data = {
            "username": "updateduser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "team": "FO",
            "password": self.user.password,  # Mantieni la password esistente
        }
        # Combina i dati iniziali con i nuovi dati
        form_data.update({k: v for k, v in initial_data.items() if k not in form_data})

        form = CustomUserChangeForm(data=form_data, instance=self.user)

        if not form.is_valid():
            print("Form errors:", form.errors)  # Per debug

        self.assertTrue(form.is_valid())

    def test_form_update_user(self):
        form = CustomUserChangeForm(instance=self.user)
        initial_data = form.initial.copy()
        form_data = {
            "username": "updateduser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "team": "FO",
            "password": self.user.password,
        }
        form_data.update({k: v for k, v in initial_data.items() if k not in form_data})

        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.first_name, "John")
        self.assertEqual(updated_user.last_name, "Doe")
        self.assertEqual(updated_user.email, "john@example.com")
        self.assertEqual(updated_user.team, "FO")

    def test_form_invalid_data(self):
        User.objects.create_user(username="anotheruser", password="testpass123")

        form = CustomUserChangeForm(instance=self.user)
        initial_data = form.initial.copy()
        form_data = {
            "username": "anotheruser",  # Username già esistente
            "email": "invalid-email",  # Email non valida
            "team": "INVALID",  # Team non valido
            "password": self.user.password,
        }
        form_data.update({k: v for k, v in initial_data.items() if k not in form_data})

        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("team", form.errors)

    def test_form_no_changes(self):
        form = CustomUserChangeForm(instance=self.user)
        initial_data = form.initial.copy()
        initial_data["password"] = (
            self.user.password
        )  # Assicurati di includere la password

        form = CustomUserChangeForm(data=initial_data, instance=self.user)

        if not form.is_valid():
            print("Form errors:", form.errors)  # Per debug

        self.assertTrue(form.is_valid())
