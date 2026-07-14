from django.urls import path

from main import api, views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),  # vaccine_list
    path("api/docs/", views.api_docs, name="api_docs"),
    path("api/", api.api_root, name="api_root"),
    path("api/vaccines/", api.vaccines_json, name="api_vaccines"),
    path("api/vaccines.csv", api.vaccines_csv, name="api_vaccines_csv"),
    path("api/diseases/", api.diseases_json, name="api_diseases"),
    path("api/diseases.csv", api.diseases_csv, name="api_diseases_csv"),
    path("vaccine/<slug:slug>/", views.VaccineDetail.as_view(), name="vaccine_detail"),
    path("disease/<slug:slug>/", views.DiseaseDetail.as_view(), name="disease_detail"),
    path("disease/", views.DiseaseList.as_view(), name="disease_list"),
    path("about/", views.about, name="about"),
]
