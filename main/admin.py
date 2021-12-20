from django.contrib import admin

from main import models


class VaccineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trade_name",
        "manufacturer",
    )
    list_display_links = ("id", "trade_name")

    ordering = ["-id"]


admin.site.register(models.Vaccine, VaccineAdmin)


class DiseaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("id", "name")

    ordering = ["-id"]


admin.site.register(models.Disease, DiseaseAdmin)
