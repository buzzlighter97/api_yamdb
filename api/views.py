from django.db.models import Avg
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed, ParseError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from slugify import slugify

from .const import (
    CATEGORIE_METHOD_PERMISSIONS,
    COMMENT_METHOD_PERMISSIONS,
    GENRE_METHOD_PERMISSIONS,
    REVIEW_METHOD_PERMISSIONS,
    TITLE_METHOD_PERMISSIONS,
)
from .filters import TitleFilterSet
from .models import Categorie, Genre, Review, Title
from .serializers import (
    CategorieSerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerNoSafeMethods,
)


def create_with_slug(self, serializer):
    """Create slug if slug not passed. Use python-slugify."""

    if not self and serializer:
        raise Http404
    if not serializer.initial_data.get('slug'):
        try:
            name = serializer.initial_data['name']
        except KeyError:
            raise ParseError
        slug = slugify(name)
        serializer.save(slug=slug)
    else:
        serializer.save()


def destroy_with_slug(self, request, **kwargs):
    """Allows you to delete models by the slug field."""

    slug = kwargs.get('pk')
    if not slug:
        raise Http404
    instance = get_object_or_404(self.queryset, slug=slug)
    self.perform_destroy(instance)
    return Response(status=HTTP_204_NO_CONTENT)


def get_obj_method_permissions(self, **kwargs):
    method = self.request.method
    try:
        permission_classes = kwargs[method]
    except KeyError:
        raise MethodNotAllowed(method)
    return (permission() for permission in permission_classes)


class ListCreateDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """A viewset that provides `create()`,  delete() and `list()` actions."""

    pass


class CategorieViewSet(ListCreateDestroyViewSet):
    """ViewSet of the Categorie model."""

    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)

    def perform_create(self, serializer):
        create_with_slug(self, serializer)

    def destroy(self, request, *args, **kwargs):
        return destroy_with_slug(self, request, *args, **kwargs)

    def get_permissions(self):
        return get_obj_method_permissions(self, **CATEGORIE_METHOD_PERMISSIONS)


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet of the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)

    def perform_create(self, serializer):
        create_with_slug(self, serializer)

    def destroy(self, request, *args, **kwargs):
        return destroy_with_slug(self, request, *args, **kwargs)

    def get_permissions(self):
        return get_obj_method_permissions(self, **GENRE_METHOD_PERMISSIONS)


class TitleViewSet(ModelViewSet):
    """ViewSet of the Title model."""

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializer
        return TitleSerializerNoSafeMethods

    def get_permissions(self):
        return get_obj_method_permissions(self, **TITLE_METHOD_PERMISSIONS)


class ReviewViewSet(ModelViewSet):
    """ViewSet of the Review model."""

    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_permissions(self):
        return get_obj_method_permissions(self, **REVIEW_METHOD_PERMISSIONS)


class CommentViewSet(ModelViewSet):
    """ViewSet of the Comment model."""

    serializer_class = CommentSerializer

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, title__id=title_id, id=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_permissions(self):
        return get_obj_method_permissions(self, **COMMENT_METHOD_PERMISSIONS)
