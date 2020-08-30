import decimal
from django.shortcuts import render
from django.http import HttpResponse

from .models import Build

# Create your views here.
def newer_version_availible(request):
    if(request.GET.get("version") is None):
        return HttpResponse(status=422)
    client_version = decimal.Decimal(request.GET.get("version"))
    newest_build = Build.objects.all().order_by("version")[0]
    if(newest_build.version > client_version):
        return HttpResponse("true")
    return HttpResponse("false")

def download_version(request):
    if(request.GET.get("version") is None):
        previous_version = 0
    else:
        previous_version = requtest.GET.get("version")
    