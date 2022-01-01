from django.contrib import messages
from django.core.mail import mail_admins
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from main import forms, models


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


def subscribe(request):
    if request.method == "POST":
        form = forms.SubscriptionForm(request.POST)
        if not form.is_valid():
            if "email" in form.errors and form.errors["email"] == [
                "Subscription with this Email already exists."
            ]:
                # if case of already subscribed
                messages.info(request, "Email already subscribed :)")
                return redirect("about")
            else:
                # all other cases
                messages.error(
                    request,
                    "Well, that didn't work :/",
                )
                return render(
                    request,
                    "main/about.html",
                    {
                        "form": form,
                    },
                )

        # this branch only executes if form is valid
        form.save()
        submitter_email = form.cleaned_data["email"]
        mail_admins(
            f"New subscription: {submitter_email}",
            f"Someone new has subscribed to allthevaccines:\n\n{submitter_email}\n",
        )
        messages.success(request, "Thanks! Email saved.")
        return redirect("about")
