from django_filters.rest_framework import (
    BaseInFilter,
    CharFilter,
    NumberFilter,
    FilterSet,
)

from .models import Title


class CharInFilter(BaseInFilter, CharFilter):
    """Проверка, что входящее значение будет разделено запятыми."""
    pass


class CategoryGenreFilter(FilterSet):
    category = CharInFilter(field_name='category__slug', lookup_expr='in')
    genre = CharInFilter(field_name='genre__slug', lookup_expr='in')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
