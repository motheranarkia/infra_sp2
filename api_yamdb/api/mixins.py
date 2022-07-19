from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class CategoryGenreMixinsViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Кастомный ViewSet на основе Mixins для чтения коллекции, создания и
    удаления экземпляров моделей.
    """

    queryset = None
    serializer_class = None
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
