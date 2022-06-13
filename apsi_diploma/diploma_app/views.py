from django.http import HttpResponse
from django.shortcuts import render

from allauth.account.decorators import login_required


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "diploma_app/home.html")


def repo(request):
    return HttpResponse(
        "Hello, welcome to the repo page."
        + request.user.username
        + str(request.user.is_authenticated)
    )


@login_required(login_url="/login")
def list(request):
    return HttpResponse("Hello, welcome to the list page.")

