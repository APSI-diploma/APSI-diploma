from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("review/", views.review_page, name="review"),
    path("add_paper/", views.add_paper_page, name="add_paper"),
]
