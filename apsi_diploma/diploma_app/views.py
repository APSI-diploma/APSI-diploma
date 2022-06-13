from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import DissertationProcess

from allauth.account.decorators import login_required


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "diploma_app/home.html")


def repo(request):
    processes = DissertationProcess.objects.filter(exam_grade__gte=3.0)

    papers = []
    for process in processes:
        paper = {
            "title": process.topic_title,
            "supervisor": process.supervisor.get_full_name(),
            "topic_description": process.topic_description,
            "paper_type": process.paper_type,
            "exam_date": process.exam_date,
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

