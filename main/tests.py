from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main.models import Disease, Vaccine


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
            vaccine_type="mRNA",
            first_authorized_year=2025,
            first_authorized_region="EU",
            first_authorization_source_url="https://example.com/authorization",
        )

        response = self.client.get(
            reverse("vaccine_detail", kwargs={"slug": vaccine.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vaccine type")
        self.assertContains(response, "mRNA")
        self.assertContains(response, "2025 (EU)")
        self.assertContains(response, "https://example.com/authorization")


class TableSortingTestCase(TestCase):
    def setUp(self):
        self.alpha_vaccine = Vaccine.objects.create(
            trade_name="Alpha vaccine",
            slug="alpha-vaccine",
            manufacturer="Zeta Labs",
            vaccine_type="mRNA",
            first_authorized_year=2020,
        )
        self.beta_vaccine = Vaccine.objects.create(
            trade_name="Beta vaccine",
            slug="beta-vaccine",
            manufacturer="Alpha Labs",
            vaccine_type="Inactivated",
        )
        self.cholera = Disease.objects.create(
            name="Cholera",
            slug="cholera",
            wikipedia_url="https://en.wikipedia.org/wiki/Cholera",
        )
        self.zika = Disease.objects.create(
            name="Zika",
            slug="zika",
            wikipedia_url="https://en.wikipedia.org/wiki/Zika_virus",
        )
        self.cholera.vaccines.add(self.alpha_vaccine, self.beta_vaccine)
        self.zika.vaccines.add(self.alpha_vaccine)

    def test_vaccine_list_toggles_text_and_computed_column_sorting(self):
        ascending = self.client.get(
            reverse("index"),
            {"sort": "manufacturer", "direction": "asc"},
        )
        descending = self.client.get(
            reverse("index"),
            {"sort": "manufacturer", "direction": "desc"},
        )
        by_disease_count = self.client.get(
            reverse("index"),
            {"sort": "disease_count", "direction": "desc"},
        )

        self.assertEqual(
            list(ascending.context["vaccine_list"].values_list("trade_name", flat=True)),
            ["Beta vaccine", "Alpha vaccine"],
        )
        self.assertEqual(
            list(
                descending.context["vaccine_list"].values_list(
                    "trade_name", flat=True
                )
            ),
            ["Alpha vaccine", "Beta vaccine"],
        )
        self.assertEqual(
            list(
                by_disease_count.context["vaccine_list"].values_list(
                    "trade_name", flat=True
                )
            ),
            ["Alpha vaccine", "Beta vaccine"],
        )
        self.assertContains(
            ascending,
            "?sort=manufacturer&amp;direction=desc",
        )
        self.assertContains(ascending, 'aria-sort="ascending"')

    def test_unknown_authorization_years_sort_last(self):
        for direction in ("asc", "desc"):
            response = self.client.get(
                reverse("index"),
                {"sort": "first_authorized", "direction": direction},
            )

            self.assertEqual(
                list(
                    response.context["vaccine_list"].values_list(
                        "trade_name", flat=True
                    )
                ),
                ["Alpha vaccine", "Beta vaccine"],
            )

    def test_invalid_sort_parameters_use_the_default_order(self):
        response = self.client.get(
            reverse("index"),
            {"sort": "manufacturer__invalid", "direction": "sideways"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sort_key"], "trade_name")
        self.assertEqual(response.context["sort_direction"], "asc")
        self.assertEqual(
            list(response.context["vaccine_list"].values_list("trade_name", flat=True)),
            ["Alpha vaccine", "Beta vaccine"],
        )

    def test_disease_list_sorts_by_vaccine_count(self):
        response = self.client.get(
            reverse("disease_list"),
            {"sort": "vaccine_count", "direction": "desc"},
        )

        self.assertEqual(
            list(response.context["disease_list"].values_list("name", flat=True)),
            ["Cholera", "Zika"],
        )
        self.assertContains(
            response,
            "?sort=vaccine_count&amp;direction=asc",
        )

    def test_disease_detail_sorts_its_vaccine_table(self):
        response = self.client.get(
            reverse("disease_detail", kwargs={"slug": self.cholera.slug}),
            {"sort": "manufacturer", "direction": "asc"},
        )

        self.assertEqual(
            list(response.context["vaccine_list"].values_list("trade_name", flat=True)),
            ["Beta vaccine", "Alpha vaccine"],
        )

    def test_disease_detail_displays_and_sorts_vaccine_types(self):
        response = self.client.get(
            reverse("disease_detail", kwargs={"slug": self.cholera.slug}),
            {"sort": "vaccine_type", "direction": "asc"},
        )

        self.assertEqual(
            list(response.context["vaccine_list"].values_list("trade_name", flat=True)),
            ["Beta vaccine", "Alpha vaccine"],
        )
        self.assertContains(response, "Inactivated")
        self.assertContains(response, "mRNA")
        self.assertContains(response, "?sort=vaccine_type&amp;direction=desc")

    def test_vaccine_detail_sorts_its_disease_table(self):
        response = self.client.get(
            reverse("vaccine_detail", kwargs={"slug": self.alpha_vaccine.slug}),
            {"sort": "wikipedia", "direction": "desc"},
        )

        self.assertEqual(
            list(response.context["disease_list"].values_list("name", flat=True)),
            ["Zika", "Cholera"],
        )

    def test_superuser_admin_header_is_sortable(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("index"))

        self.assertContains(response, "?sort=admin&amp;direction=asc")


class DiseaseSummaryTestCase(TestCase):
    def setUp(self):
        self.disease = Disease.objects.create(
            name="Example disease",
            slug="example-disease",
            wikipedia_url="https://en.wikipedia.org/wiki/Example",
        )
        vaccines = [
            Vaccine.objects.create(
                trade_name="Early One",
                slug="early-one",
                manufacturer="Example Labs",
                vaccine_type="mRNA",
                first_authorized_year=1999,
                first_authorized_region="United Kingdom",
                first_authorization_source_url="https://example.com/early-one",
            ),
            Vaccine.objects.create(
                trade_name="Early Two",
                slug="early-two",
                manufacturer="Example Labs",
                vaccine_type="mRNA",
                first_authorized_year=1999,
                first_authorized_region="United States",
                first_authorization_source_url="https://example.com/early-two",
            ),
            Vaccine.objects.create(
                trade_name="Later Vaccine",
                slug="later-vaccine",
                manufacturer="Example Labs",
                vaccine_type="Viral vector",
                first_authorized_year=2005,
                first_authorized_region="European Union",
                first_authorization_source_url="https://example.com/later-vaccine",
            ),
            Vaccine.objects.create(
                trade_name="Undated Vaccine",
                slug="undated-vaccine",
                manufacturer="Example Labs",
            ),
        ]
        self.disease.vaccines.add(*vaccines)

    def test_disease_page_calculates_authorization_history(self):
        response = self.client.get(
            reverse("disease_detail", kwargs={"slug": self.disease.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vaccine_count"], 4)
        self.assertEqual(response.context["undated_vaccine_count"], 1)
        self.assertEqual(
            [group["year"] for group in response.context["authorization_history"]],
            [1999, 2005],
        )
        self.assertNotContains(response, "At a glance")
        self.assertNotContains(response, "Technology breakdown")
        self.assertNotContains(response, "<progress")
        self.assertContains(response, "Authorization history")
        self.assertContains(response, "https://example.com/early-one")
        self.assertContains(response, "Later Vaccine")
        self.assertContains(response, "Authorization year unknown")
        self.assertNotContains(response, "1 product")
        self.assertNotContains(response, "2 products")
        self.assertNotContains(response, "<details")
        content = response.content.decode()
        self.assertLess(
            content.index("Vaccines (4)"),
            content.index("Authorization history"),
        )

    def test_empty_disease_page_has_clear_authorization_empty_state(self):
        empty_disease = Disease.objects.create(
            name="Empty disease",
            slug="empty-disease",
            wikipedia_url="https://en.wikipedia.org/wiki/Empty_set",
        )

        response = self.client.get(
            reverse("disease_detail", kwargs={"slug": empty_disease.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vaccine_count"], 0)
        self.assertEqual(response.context["authorization_history"], [])
        self.assertNotContains(response, "Technology breakdown")
        self.assertContains(
            response,
            "No documented authorization years are available yet.",
        )
