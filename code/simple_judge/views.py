from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)

# Create your views here.
def index(request) -> HttpResponse:
    return render(request, "index.html")