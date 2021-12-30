from django.urls import path

from main import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),  # vaccine_list
    path("vaccine/<slug:slug>/", views.VaccineDetail.as_view(), name="vaccine_detail"),
    path("disease/<slug:slug>/", views.DiseaseDetail.as_view(), name="disease_detail"),
    path("disease/", views.DiseaseList.as_view(), name="disease_list"),
    path("about/", views.about, name="about"),
]
