from itertools import groupby

from django.shortcuts import render
from django.db.models import Count, F
from django.views.generic import DetailView, ListView

from main import models


class SortableTableMixin:
    sort_fields = {}
    default_sort = ""

    def get_sorting(self):
        sort_key = self.request.GET.get("sort", self.default_sort)
        if sort_key not in self.sort_fields:
            sort_key = self.default_sort

        direction = self.request.GET.get("direction", "asc")
        if direction not in {"asc", "desc"}:
            direction = "asc"

        return sort_key, direction

    def sort_queryset(self, queryset):
        sort_key, direction = self.get_sorting()
        field_name = self.sort_fields[sort_key]
        expression = F(field_name)
        if direction == "desc":
            expression = expression.desc(nulls_last=True)
        else:
            expression = expression.asc(nulls_last=True)

        ordering = [expression]
        if field_name != "pk":
            ordering.append("pk")
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_key"], context["sort_direction"] = self.get_sorting()
        return context


class Index(SortableTableMixin, ListView):
    model = models.Vaccine
    template_name = "main/index.html"
    sort_fields = {
        "trade_name": "trade_name",
        "manufacturer": "manufacturer",
        "first_authorized": "first_authorized_year",
        "disease_count": "disease_count",
        "admin": "pk",
    }
    default_sort = "trade_name"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            disease_count=Count("disease", distinct=True)
        )
        return self.sort_queryset(queryset.prefetch_related("disease_set"))


class DiseaseDetail(SortableTableMixin, DetailView):
    model = models.Disease
    sort_fields = {
        "trade_name": "trade_name",
        "manufacturer": "manufacturer",
        "vaccine_type": "vaccine_type",
        "admin": "pk",
    }
    default_sort = "trade_name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = models.Vaccine.objects.filter(disease=self.object)

        vaccine_count = queryset.count()
        authorized_vaccines = list(
            queryset.filter(first_authorized_year__isnull=False).order_by(
                "first_authorized_year", "trade_name"
            )
        )
        authorization_history = [
            {
                "year": year,
                "vaccines": list(vaccines),
            }
            for year, vaccines in groupby(
                authorized_vaccines,
                key=lambda vaccine: vaccine.first_authorized_year,
            )
        ]

        context["vaccine_list"] = self.sort_queryset(queryset)
        context["vaccine_count"] = vaccine_count
        context["undated_vaccines"] = queryset.filter(
            first_authorized_year__isnull=True
        ).order_by("trade_name")
        context["undated_vaccine_count"] = vaccine_count - len(authorized_vaccines)
        context["authorization_history"] = authorization_history
        return context


class DiseaseList(SortableTableMixin, ListView):
    model = models.Disease
    sort_fields = {
        "name": "name",
        "vaccine_count": "vaccine_count",
        "wikipedia": "wikipedia_url",
        "admin": "pk",
    }
    default_sort = "name"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            vaccine_count=Count("vaccines", distinct=True)
        )
        return self.sort_queryset(queryset)


class VaccineDetail(SortableTableMixin, DetailView):
    model = models.Vaccine
    sort_fields = {
        "name": "name",
        "wikipedia": "wikipedia_url",
        "admin": "pk",
    }
    default_sort = "name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = models.Disease.objects.filter(vaccines=self.object)
        context["disease_list"] = self.sort_queryset(queryset)
        return context


def about(request):
    return render(request, "main/about.html")


def api_docs(request):
    return render(
        request,
        "main/api_docs.html",
        {
            "vaccine_count": models.Vaccine.objects.count(),
            "disease_count": models.Disease.objects.count(),
        },
    )
