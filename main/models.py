from django.db import models


class Vaccine(models.Model):
    trade_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    class Meta:
        ordering = ["trade_name"]

    def __str__(self):
        return self.trade_name


class Disease(models.Model):
    name = models.CharField(max_length=100)
    wikipedia_url = models.CharField(max_length=100)
    vaccines = models.ManyToManyField(Vaccine)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
