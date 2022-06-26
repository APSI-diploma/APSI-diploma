from django.urls import include, path
from . import views


urlpatterns = [
    path("repo/", views.repo, name="repo"),
    path("repo/self/", views.list, name="list"),
]
