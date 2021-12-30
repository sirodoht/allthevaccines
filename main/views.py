from django.shortcuts import render
from django.views.generic import DetailView, ListView

from main import models


class Index(ListView):
    model = models.Vaccine
    template_name = "main/index.html"


class DiseaseDetail(DetailView):
    model = models.Disease

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vaccine_list"] = models.Vaccine.objects.filter(disease=self.object)
        return context


class DiseaseList(ListView):
    model = models.Disease


class VaccineDetail(DetailView):
    model = models.Vaccine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disease_list"] = models.Disease.objects.filter(vaccines=self.object)
        return context


def about(request):
    return render(request, "main/about.html")
