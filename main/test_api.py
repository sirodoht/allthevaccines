import csv
import io

from django.test import TestCase
from django.urls import reverse

from main.models import Disease, Vaccine


class PublicApiTestCase(TestCase):
    def setUp(self):
        self.vaccine = Vaccine.objects.create(
            trade_name="Example vaccine",
            slug="example-vaccine",
            manufacturer="Example Labs",
            vaccine_class="Recombinant",
            vaccine_type="Protein subunit",
            first_authorized_year=2024,
            first_authorized_region="Example region",
            first_authorization_source_url="https://example.com/authorization",
            info_urls="https://example.com/one\nhttps://example.com/two",
        )
        self.disease = Disease.objects.create(
            name="Example disease",
            slug="example-disease",
            wikipedia_url="https://en.wikipedia.org/wiki/Example",
            notes="First line, with a comma.\nSecond line.",
        )
        self.disease.vaccines.add(self.vaccine)

    def test_api_root_discovers_collections_and_downloads(self):
        response = self.client.get(reverse("api_root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "*")
        self.assertEqual(response["Cache-Control"], "public, max-age=300")
        self.assertEqual(response.json()["schema_version"], 1)
        self.assertEqual(
            response.json()["endpoints"]["vaccines"],
            "http://testserver/api/vaccines/",
        )
        self.assertEqual(
            response.json()["downloads"]["diseases_csv"],
            "http://testserver/api/diseases.csv",
        )

    def test_vaccine_json_exposes_complete_record_and_relationships(self):
        response = self.client.get(reverse("api_vaccines"))
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertNotIn("Content-Disposition", response)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["count"], 1)
        self.assertEqual(
            payload["results"][0],
            {
                "id": self.vaccine.pk,
                "trade_name": "Example vaccine",
                "slug": "example-vaccine",
                "manufacturer": "Example Labs",
                "vaccine_class": "Recombinant",
                "vaccine_type": "Protein subunit",
                "first_authorized_year": 2024,
                "first_authorized_region": "Example region",
                "first_authorization_source_url": "https://example.com/authorization",
                "info_urls": [
                    "https://example.com/one",
                    "https://example.com/two",
                ],
                "diseases": [
                    {
                        "id": self.disease.pk,
                        "name": "Example disease",
                        "slug": "example-disease",
                    }
                ],
            },
        )

    def test_json_download_has_a_stable_filename(self):
        response = self.client.get(reverse("api_vaccines"), {"download": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="allthevaccines-vaccines.json"',
        )

    def test_vaccine_csv_is_a_parseable_named_download(self):
        response = self.client.get(reverse("api_vaccines_csv"))
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="allthevaccines-vaccines.csv"',
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["trade_name"], "Example vaccine")
        self.assertEqual(rows[0]["first_authorized_year"], "2024")
        self.assertEqual(rows[0]["disease_count"], "1")
        self.assertEqual(rows[0]["diseases"], "Example disease")
        self.assertEqual(
            rows[0]["info_urls"],
            "https://example.com/one | https://example.com/two",
        )

    def test_disease_json_exposes_notes_count_and_vaccines(self):
        response = self.client.get(reverse("api_diseases"))
        record = response.json()["results"][0]

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(record["notes"], "First line, with a comma.\nSecond line.")
        self.assertEqual(record["vaccine_count"], 1)
        self.assertEqual(
            record["vaccines"],
            [
                {
                    "id": self.vaccine.pk,
                    "trade_name": "Example vaccine",
                    "slug": "example-vaccine",
                }
            ],
        )

    def test_disease_csv_preserves_multiline_notes(self):
        response = self.client.get(reverse("api_diseases_csv"))
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["notes"], "First line, with a comma.\nSecond line.")
        self.assertEqual(rows[0]["vaccine_count"], "1")
        self.assertEqual(rows[0]["vaccines"], "Example vaccine")

    def test_collection_pages_link_to_api_and_downloads(self):
        vaccine_page = self.client.get(reverse("index"))
        disease_page = self.client.get(reverse("disease_list"))

        self.assertContains(vaccine_page, reverse("api_vaccines"))
        self.assertContains(vaccine_page, reverse("api_vaccines_csv"))
        self.assertContains(disease_page, reverse("api_diseases"))
        self.assertContains(disease_page, reverse("api_diseases_csv"))

    def test_api_is_read_only(self):
        response = self.client.post(reverse("api_vaccines"), data={})

        self.assertEqual(response.status_code, 405)

    def test_api_docs_are_available_from_the_global_navigation(self):
        docs = self.client.get(reverse("api_docs"))
        index = self.client.get(reverse("index"))

        self.assertEqual(docs.status_code, 200)
        self.assertContains(docs, "API Documentation")
        self.assertContains(docs, reverse("api_vaccines"))
        self.assertContains(docs, reverse("api_diseases_csv"))
        self.assertContains(index, reverse("api_docs"))
