from django.http import HttpResponse
import datetime
from django.utils import timezone


def home(request):
    now_date = datetime.datetime.now()
    now_timezone = timezone.now()
    return HttpResponse(f"datetime = {now_date}         timezone = {now_timezone}")