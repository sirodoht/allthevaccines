from django.views.generic import ListView

from main import models


class IndexView(ListView):
    model = models.Vaccine
    template_name = "main/index.html"
