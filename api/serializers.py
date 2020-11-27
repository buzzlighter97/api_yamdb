from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Categorie, Comment, Genre, Review, Title


class CategorieSerializer(serializers.ModelSerializer):
    """Serializer for categorie models."""

    class Meta:
        exclude = ('id',)
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre models."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for title models."""

    category = CategorieSerializer(read_only=True,)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True,)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerNoSafeMethods(serializers.ModelSerializer):
    """Serializer for title models, no Safe methods."""

    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(),
        slug_field='slug',
        default=None,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment models."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ('review',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review models."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ('title',)
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if not request.method == 'POST':
            return data

        title_id = request.parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, id=title_id)
        if title.reviews.filter(author=request.user).exists():
            raise serializers.ValidationError(
                'Your review for this title is already exists'
            )
        return data
