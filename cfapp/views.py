# from django.http import HttpResponse
# import datetime
# from django.utils import timezone

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




# def home(request):
#     now_date = datetime.datetime.now()
#     now_timezone = timezone.now()
#     return HttpResponse(f"datetime = {now_date}         timezone = {now_timezone}")