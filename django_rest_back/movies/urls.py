from django.urls import path

from . import views


urlpatterns = [
    path("movie/", views.MoviesListView.as_view()),
    path("movie/<int:pk>/", views.MoviesDetailView.as_view()),

]
