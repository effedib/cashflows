from django.urls import path

from .views import (
    IncassoListView,
    IncassoDetailView,
    IncassoCreateView,
    IncassoUpdateView,
    IncassoDeleteView,
    TransazioneListView,
    TransazioneDetailView,
    TransazioneCreateView,
    TransazioneUpdateView,
    TransazioneDeleteView,
)

urlpatterns = [
    path("incassi/", IncassoListView.as_view(), name="incassi_view"),
    path("incassi/new/", IncassoCreateView.as_view(), name="incasso_new_view"),
    path("incassi/<str:pk>/", IncassoDetailView.as_view(), name="incasso_detail_view"),
    path("incassi/<int:pk>/edit/", IncassoUpdateView.as_view(), name="incasso_edit_view"),
    path("incassi/<int:pk>/delete/", IncassoDeleteView.as_view(), name="incasso_delete_view"),
    path("transazioni/", TransazioneListView.as_view(), name="transazioni_view"),
    path("transazioni/new/", TransazioneCreateView.as_view(), name="transazione_new_view"),
    path("transazioni/<str:pk>/", TransazioneDetailView.as_view(), name="transazione_detail_view"),
    path("transazioni/<int:pk>/edit/", TransazioneUpdateView.as_view(), name="transazione_edit_view"),
    path("transazioni/<int:pk>/delete/", TransazioneDeleteView.as_view(), name="transazione_delete_view"),
]
