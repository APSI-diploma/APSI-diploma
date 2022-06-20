from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import DissertationProcess
import django_filters

from allauth.account.decorators import login_required


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "diploma_app/home.html")


def repo(request):
    processes = DissertationProcess.objects.filter(exam_grade__gte=3.0)

    if "key_words" in request.GET:
        keyords = request.GET["key_words"].split(",")
        for keyword in keyords:
            processes = processes.filter(keywords__contains=keyword)

    if "title" in request.GET:
        processes = processes.filter(topic_title__contains=request.GET["title"])

    if "exam_after" in request.GET:
        processes = processes.filter(exam_date__gte=request.GET["exam_after"])

    if "exam_before" in request.GET:
        processes = processes.filter(exam_date__lte=request.GET["exam_before"])

    papers = []
    for process in processes:
        paper = {
            "author": "autor pracy",  # TODO wyciągnąć autora
            "title": process.topic_title,
            "supervisor": process.supervisor.get_full_name(),
            "topic_description": process.topic_description,
            "paper_type": process.paper_type,
            "exam_date": process.exam_date.strftime("%Y-%m-%d"),
            "exam_grade": process.exam_grade,
            "keywords": process.keywords,
        }
        papers.append(paper)
    context = {"processes": papers}

    return HttpResponse(
        "Hello, welcome to the repo page."
        + request.user.username
        + str(request.user.is_authenticated)
        + "\n"
        + str(context)
    )


@login_required(login_url="/login")
def list(request):
    return HttpResponse("Hello, welcome to the list page.")

