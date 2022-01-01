from django.contrib import admin

from main import models


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


admin.site.register(models.Vaccine, VaccineAdmin)


class DiseaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "name",
    )
    list_display_links = ("id", "slug")

    ordering = ["-id"]


admin.site.register(models.Disease, DiseaseAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "created_at",
        "unsubscribe_key",
    )
    list_display_links = ("id", "email")

    ordering = ["-id"]


admin.site.register(models.Subscription, SubscriptionAdmin)
