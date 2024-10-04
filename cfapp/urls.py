from django.urls import path

from .views import (
    IncassoListView,
    IncassoDetailView,
    IncassoCreateView,
    IncassoUpdateView,
    IncassoDeleteView,
    )

urlpatterns = [
    path("", IncassoListView.as_view(), name="incassi_view"),
    path("new/", IncassoCreateView.as_view(), name="incasso_new_view"),
    path("<str:pk>/", IncassoDetailView.as_view(), name="incasso_detail_view"),
    path("<int:pk>/edit/", IncassoUpdateView.as_view(), name="incasso_edit_view"),
    path("<int:pk>/delete/", IncassoDeleteView.as_view(), name="incasso_delete_view"),
]