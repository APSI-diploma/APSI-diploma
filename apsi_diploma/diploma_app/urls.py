from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.home_page, name="home"),
    path("repo/", views.repo, name="repo"),
    path("repo/self/", views.list, name="list"),
]
