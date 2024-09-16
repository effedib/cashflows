from django.urls import path

from . import views

urlpatterns = [
    path("incassi/", views.IncassoListView.as_view(), name="incassi_view"),
]