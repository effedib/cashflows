from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .models import Incasso
from .tables import IncassoTable
from .filters import IncassoFilter


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("incassi_view")


class IncassoListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    table_class = IncassoTable
    model = Incasso
    template_name = "cfapp/incasso_table.html"
    filterset_class = IncassoFilter
    export_name = "esport_incassi"
    exclude_columns = ["_", "__"]


class IncassoCreateView(LoginRequiredMixin, CreateView):
    model = Incasso
    template_name = "cfapp/incasso_new.html"
    fields = "__all__"
    success_url = reverse_lazy("incassi_view")


class IncassoUpdateView(LoginRequiredMixin, UpdateView):
    model = Incasso
    template_name = "cfapp/incasso_edit.html"
    fields = "__all__"
    success_url = reverse_lazy("incassi_view")


class IncassoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Incasso
    template_name = "cfapp/incasso_delete.html"
    success_url = reverse_lazy("incassi_view")


class IncassoDetailView(LoginRequiredMixin, DetailView):
    model = Incasso
    template_name = "cfapp/incasso_detail.html"

    def get_object(self):
        return get_object_or_404(Incasso, ricevuta=self.kwargs["pk"])
