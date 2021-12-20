from django.urls import path

from main import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
