from rest_framework import serializers

from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    "List of movies"

    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")

class MovieDetailSerializer(serializers.ModelSerializer):
    "Whole movie"

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ("draft", ) #show all lines except draft

