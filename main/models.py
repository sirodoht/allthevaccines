from django.db import models


class Vaccine(models.Model):
    trade_name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    info_urls = models.TextField(null=True, blank=True)
    vaccine_class = models.CharField(max_length=100, null=True, blank=True)

    @property
    def wikipedia_url_fancy(self):
        return "wikipedia:" + self.wikipedia_url[30:]

    class Meta:
        ordering = ["trade_name"]

    def __str__(self):
        return self.trade_name


class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    wikipedia_url = models.CharField(max_length=100)
    vaccines = models.ManyToManyField(Vaccine, blank=True)

    @property
    def wikipedia_url_fancy(self):
        return "wikipedia:" + self.wikipedia_url[30:]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
