from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .models import Incasso
from .tables import IncassoTable
from .filters import IncassoFilter

class IncassoListView(SingleTableMixin, FilterView):
    table_class = IncassoTable
    model = Incasso
    template_name = "cfapp/incasso_table.html"
    filterset_class = IncassoFilter


class IncassoCreateView(CreateView):
    model = Incasso
    template_name = "cfapp/incasso_new.html"
    fields = "__all__"


class IncassoUpdateView(UpdateView):
    model = Incasso
    template_name = "cfapp/incasso_edit.html"
    fields = "__all__"


class IncassoDeleteView(DeleteView):
    model = Incasso
    template_name = "cfapp/incasso_delete.html"
    success_url = reverse_lazy("incassi_view")


def incasso_detail(request, pk):
    incasso = get_object_or_404(Incasso, ricevuta=pk)
    return render(request, "cfapp/incasso_detail.html", {"incasso": incasso})