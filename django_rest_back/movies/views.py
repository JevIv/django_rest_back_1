from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import models
from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer)
from .service import get_client_ip


class MoviesListView(APIView):
    """Render list of movies"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                "ratings",
                filter=models.Q(ratings__ip=get_client_ip((request)))
            ).annotate(middle_star=models.Sum(models.F('ratings_star')) / models.Count(models.F('ratings')))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MoviesDetailView(APIView):
    """Render movie"""
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Add review to movie"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Add star to movie"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """View actors list"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """View actors list"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

