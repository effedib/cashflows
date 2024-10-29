from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .models import Incasso, Transazione
from .tables import IncassoTable, TransazioneTable
from .filters import IncassoFilter, TransazioneFilter
from .forms import TransazioneForm, IncassoForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("incassi_view")


class IncassoListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    table_class = IncassoTable
    model = Incasso
    template_name = "cfapp/incassi/incasso_table.html"
    filterset_class = IncassoFilter
    export_name = "esport_incassi"
    exclude_columns = ["_", "__"]


class IncassoCreateView(LoginRequiredMixin, CreateView):
    model = Incasso
    form_class = IncassoForm
    template_name = "cfapp/incassi/incasso_new.html"
    success_url = reverse_lazy("incassi_view")


class IncassoUpdateView(LoginRequiredMixin, UpdateView):
    model = Incasso
    form_class = IncassoForm
    template_name = "cfapp/incassi/incasso_edit.html"
    success_url = reverse_lazy("incassi_view")


class IncassoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Incasso
    template_name = "cfapp/incassi/incasso_delete.html"
    success_url = reverse_lazy("incassi_view")


class IncassoDetailView(LoginRequiredMixin, DetailView):
    model = Incasso
    template_name = "cfapp/incassi/incasso_detail.html"

    def get_object(self):
        return get_object_or_404(Incasso, ricevuta=self.kwargs["pk"])


class TransazioneListView(
    LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView
):
    table_class = TransazioneTable
    model = Transazione
    template_name = "cfapp/transazioni/transazione_table.html"
    filterset_class = TransazioneFilter
    export_name = "esport_transazioni"
    exclude_columns = ["_", "__", "___"]


class TransazioneCreateView(LoginRequiredMixin, CreateView):
    model = Transazione
    form_class = TransazioneForm
    template_name = "cfapp/transazioni/transazione_new.html"
    success_url = reverse_lazy("transazioni_view")


class TransazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = Transazione
    form_class = TransazioneForm
    template_name = "cfapp/transazioni/transazione_edit.html"
    success_url = reverse_lazy("transazioni_view")


class TransazioneDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Transazione
    template_name = "cfapp/transazioni/transazione_delete.html"
    success_url = reverse_lazy("transazioni_view")


class TransazioneDetailView(LoginRequiredMixin, DetailView):
    model = Transazione
    template_name = "cfapp/transazioni/transazione_detail.html"

    def get_object(self):
        return get_object_or_404(Transazione, id=self.kwargs["pk"])
