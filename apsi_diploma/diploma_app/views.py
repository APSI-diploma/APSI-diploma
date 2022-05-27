from django.shortcuts import render

from django.http import HttpRequest

from allauth.account.decorators import login_required


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "diploma_app/home.html")


@login_required(login_url="/login")
def review_page(request: HttpRequest):
    return render(request, "diploma_app/review.html")


@login_required(login_url="/login")
def add_paper_page(request: HttpRequest):
    return render(request, "diploma_app/add_paper.html")
