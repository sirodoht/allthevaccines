import csv

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from main.models import Disease, Vaccine


API_SCHEMA_VERSION = 1
API_CACHE_CONTROL = "public, max-age=300"


def _public_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Cache-Control"] = API_CACHE_CONTROL
    return response


def _json_response(payload, filename=None):
    response = JsonResponse(
        payload,
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
    if filename:
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return _public_response(response)


def _csv_response(filename):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return _public_response(response)


def _info_urls(vaccine):
    if not vaccine.info_urls:
        return []
    return [url.strip() for url in vaccine.info_urls.splitlines() if url.strip()]


def _serialize_vaccine(vaccine):
    return {
        "id": vaccine.pk,
        "trade_name": vaccine.trade_name,
        "slug": vaccine.slug,
        "manufacturer": vaccine.manufacturer,
        "vaccine_class": vaccine.vaccine_class,
        "vaccine_type": vaccine.vaccine_type,
        "first_authorized_year": vaccine.first_authorized_year,
        "first_authorized_region": vaccine.first_authorized_region,
        "first_authorization_source_url": vaccine.first_authorization_source_url,
        "info_urls": _info_urls(vaccine),
        "diseases": [
            {
                "id": disease.pk,
                "name": disease.name,
                "slug": disease.slug,
            }
            for disease in vaccine.disease_set.all()
        ],
    }


def _serialize_disease(disease):
    return {
        "id": disease.pk,
        "name": disease.name,
        "slug": disease.slug,
        "wikipedia_url": disease.wikipedia_url,
        "notes": disease.notes,
        "vaccine_count": disease.vaccine_count,
        "vaccines": [
            {
                "id": vaccine.pk,
                "trade_name": vaccine.trade_name,
                "slug": vaccine.slug,
            }
            for vaccine in disease.vaccines.all()
        ],
    }


@require_GET
def api_root(request):
    def absolute_url(name, query=""):
        url = request.build_absolute_uri(reverse(name))
        return f"{url}{query}"

    return _json_response(
        {
            "name": "allthevaccines API",
            "schema_version": API_SCHEMA_VERSION,
            "endpoints": {
                "vaccines": absolute_url("api_vaccines"),
                "diseases": absolute_url("api_diseases"),
            },
            "downloads": {
                "vaccines_json": absolute_url("api_vaccines", "?download=1"),
                "vaccines_csv": absolute_url("api_vaccines_csv"),
                "diseases_json": absolute_url("api_diseases", "?download=1"),
                "diseases_csv": absolute_url("api_diseases_csv"),
            },
        }
    )


@require_GET
def vaccines_json(request):
    queryset = Vaccine.objects.prefetch_related("disease_set")
    results = [_serialize_vaccine(vaccine) for vaccine in queryset]
    filename = (
        "allthevaccines-vaccines.json" if request.GET.get("download") == "1" else None
    )
    return _json_response(
        {
            "schema_version": API_SCHEMA_VERSION,
            "count": len(results),
            "results": results,
        },
        filename=filename,
    )


@require_GET
def vaccines_csv(request):
    response = _csv_response("allthevaccines-vaccines.csv")
    writer = csv.writer(response, lineterminator="\n")
    writer.writerow(
        [
            "id",
            "trade_name",
            "slug",
            "manufacturer",
            "vaccine_class",
            "vaccine_type",
            "first_authorized_year",
            "first_authorized_region",
            "first_authorization_source_url",
            "disease_count",
            "diseases",
            "disease_slugs",
            "info_urls",
        ]
    )
    for vaccine in Vaccine.objects.prefetch_related("disease_set"):
        diseases = list(vaccine.disease_set.all())
        writer.writerow(
            [
                vaccine.pk,
                vaccine.trade_name,
                vaccine.slug,
                vaccine.manufacturer,
                vaccine.vaccine_class or "",
                vaccine.vaccine_type or "",
                vaccine.first_authorized_year or "",
                vaccine.first_authorized_region or "",
                vaccine.first_authorization_source_url or "",
                len(diseases),
                " | ".join(disease.name for disease in diseases),
                " | ".join(disease.slug for disease in diseases),
                " | ".join(_info_urls(vaccine)),
            ]
        )
    return response


@require_GET
def diseases_json(request):
    queryset = Disease.objects.annotate(
        vaccine_count=Count("vaccines", distinct=True)
    ).prefetch_related("vaccines")
    results = [_serialize_disease(disease) for disease in queryset]
    filename = (
        "allthevaccines-diseases.json" if request.GET.get("download") == "1" else None
    )
    return _json_response(
        {
            "schema_version": API_SCHEMA_VERSION,
            "count": len(results),
            "results": results,
        },
        filename=filename,
    )


@require_GET
def diseases_csv(request):
    response = _csv_response("allthevaccines-diseases.csv")
    writer = csv.writer(response, lineterminator="\n")
    writer.writerow(
        [
            "id",
            "name",
            "slug",
            "wikipedia_url",
            "notes",
            "vaccine_count",
            "vaccines",
            "vaccine_slugs",
        ]
    )
    queryset = Disease.objects.annotate(
        vaccine_count=Count("vaccines", distinct=True)
    ).prefetch_related("vaccines")
    for disease in queryset:
        vaccines = list(disease.vaccines.all())
        writer.writerow(
            [
                disease.pk,
                disease.name,
                disease.slug,
                disease.wikipedia_url,
                disease.notes or "",
                disease.vaccine_count,
                " | ".join(vaccine.trade_name for vaccine in vaccines),
                " | ".join(vaccine.slug for vaccine in vaccines),
            ]
        )
    return response
