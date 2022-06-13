from django.urls import path
from . import views


urlpatterns = [
    path("", views.repo, name="repo"),
    path("self/", views.list, name="list"),
]

