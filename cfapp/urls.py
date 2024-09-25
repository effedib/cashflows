from django.urls import path

from .views import (
    IncassoListView,
    incasso_detail,
    IncassoCreateView,
    IncassoUpdateView,
    IncassoDeleteView,
    )

urlpatterns = [
    path("", IncassoListView.as_view(), name="incassi_view"),
    path("new/", IncassoCreateView.as_view(), name="incasso_new_view"),
    path("<str:pk>/", incasso_detail, name="incasso_detail_view"),
    path("<int:pk>/edit/", IncassoUpdateView.as_view(), name="incasso_edit_view"),
    path("<int:pk>/delete/", IncassoDeleteView.as_view(), name="incasso_delete_view"),
]