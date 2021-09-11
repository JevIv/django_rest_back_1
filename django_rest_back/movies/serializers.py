from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    """List of movies"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")


class FilterReviewSerializer(serializers.ListSerializer):
    """Comments filter of parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Show recursive children(tree)"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.Serializer):
    """Show actors and directors"""

    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.Serializer):
    """Detailed info about actors or directors"""

    class Meta:
        model = Actor
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add Review"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Show Reviews"""

    children = RecursiveSerializer(many=True)

    class Meta:
        model = Review
        fields = ("name", "text", "children")
        list_serializer_class = FilterReviewSerializer


class MovieDetailSerializer(serializers.ModelSerializer):
    """Whole movie"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", ) #show all lines except draft


class CreateRatingSerializer(serializers.ModelSerializer):
    """Add rating by user"""

    class Meta:
        model = Rating
        fields = ("star", "movie" ) #show all lines except draft

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")},
        )
        return rating
