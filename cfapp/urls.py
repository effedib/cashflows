from django.urls import path

from .views import (
    IncassoListView,
    incasso_detail,
    IncassoCreateView,
    IncassoUpdateView,
    IncassoDeleteView,
    )

urlpatterns = [
    path("incassi/", IncassoListView.as_view(), name="incassi_view"),
    path("incassi/new/", IncassoCreateView.as_view(), name="incasso_new_view"),
    path("incassi/<str:pk>/", incasso_detail, name="incasso_detail_view"),
    path("incassi/<int:pk>/edit/", IncassoUpdateView.as_view(), name="incasso_edit_view"),
    path("incassi/<int:pk>/delete/", IncassoDeleteView.as_view(), name="incasso_delete_view"),
]