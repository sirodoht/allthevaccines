import uuid

import markdown
from django.db import models


class Vaccine(models.Model):
    trade_name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    info_urls = models.TextField(null=True, blank=True)
    vaccine_class = models.CharField(max_length=100, null=True, blank=True)
    vaccine_type = models.CharField(max_length=100, null=True, blank=True)

    @property
    def wikipedia_url_fancy(self):
        return "wikipedia:" + self.wikipedia_url[30:]

    @property
    def info_urls_html(self):
        if not self.info_urls:
            return "<em>no links</em>"
        url_list = self.info_urls.split("\n")
        # join all formatted links with <br> in between
        return "<br>".join(f'<a href="{url}">{url}</a>' for url in url_list)

    class Meta:
        ordering = ["trade_name"]

    def __str__(self):
        return self.trade_name


class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    wikipedia_url = models.CharField(max_length=100)
    vaccines = models.ManyToManyField(Vaccine, blank=True)
    notes = models.TextField(null=True, blank=True)

    @property
    def wikipedia_url_fancy(self):
        return "wikipedia:" + self.wikipedia_url[30:].replace("_", " ")

    @property
    def notes_html(self):
        if not self.notes:
            return "<em>no notes</em>"
        return markdown.markdown(
            self.notes,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.footnotes",
            ],
        )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
