from django_filters import rest_framework

from .models import Title


class TitleFilterSet(rest_framework.FilterSet):
    """Filter for Title models.

    fields: year, genre__slug, category__slug: exact filter
    field: name: contains filter
    """

    year = rest_framework.NumberFilter(field_name='year')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'category',
            'genre',
        )
