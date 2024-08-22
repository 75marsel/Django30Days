from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("search/", views.search_results, name="search"),
]
