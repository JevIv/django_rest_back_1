from rest_framework import generics

from django.db import models
from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer)
from .service import get_client_ip


class MoviesListView(generics.ListAPIView):
    """Render list of movies"""

    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                "ratings",
                filter=models.Q(ratings__ip=get_client_ip((self.request)))
            ).annotate(middle_star=models.Sum(models.F('ratings_star')) / models.Count(models.F('ratings')))
        )
        return movies


class MoviesDetailView(generics.RetrieveAPIView):
    """Render movie"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.RetrieveAPIView):
    """Add review to movie"""

    serializer_class = ReviewCreateSerializer



class AddStarRatingView(generics.CreateAPIView):
    """Add star to movie"""

    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorsListView(generics.ListAPIView):
    """View actors list"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """View actors list"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

