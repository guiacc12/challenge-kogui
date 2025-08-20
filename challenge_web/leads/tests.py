from django.test import TestCase
from django.urls import reverse
from .models import Lead


class LeadModelTest(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(name="Test User", email="test@example.com")

    def test_lead_creation(self):
        self.assertEqual(self.lead.name, "Test User")
        self.assertEqual(self.lead.email, "test@example.com")

    def test_lead_str(self):
        self.assertEqual(str(self.lead), "Test User")

    def test_lead_creation_timestamp(self):
        self.assertIsNotNone(self.lead.created_at)


class LeadFormViewTests(TestCase):
    def test_get_form_page(self):
        response = self.client.get(reverse('lead_form'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_lead(self):
        data = {"name": "User", "email": "user@example.com", "telefone": ""}
        response = self.client.post(reverse('lead_form'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lead.objects.filter(email="user@example.com").exists())