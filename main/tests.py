from django.test import TestCase
from django.urls import reverse

from main.models import Vaccine


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "allthevaccines")


class AboutTestCase(TestCase):
    def test_about(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")


class VaccineAuthorizationTestCase(TestCase):
    def test_vaccine_detail_displays_first_authorization(self):
        vaccine = Vaccine.objects.create(
            trade_name="Example vaccine",
            slug="example-vaccine",
            manufacturer="Example manufacturer",
            first_authorized_year=2025,
            first_authorized_region="EU",
            first_authorization_source_url="https://example.com/authorization",
        )

        response = self.client.get(
            reverse("vaccine_detail", kwargs={"slug": vaccine.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2025 (EU)")
        self.assertContains(response, "https://example.com/authorization")
