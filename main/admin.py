from django.contrib import admin

from main import models


@admin.register(models.Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "trade_name",
        "manufacturer",
    )
    list_display_links = ("id", "slug")
    list_per_page = 200

    ordering = ["-id"]


@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "name",
    )
    list_display_links = ("id", "slug")

    ordering = ["-id"]
