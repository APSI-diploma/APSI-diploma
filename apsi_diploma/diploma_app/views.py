from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def repo(request):
    return HttpResponse(
        "Hello, welcome to the repo page."
        + request.user.username
        + str(request.user.is_authenticated)
    )


def list(request):
    return HttpResponse("Hello, welcome to the list page.")

