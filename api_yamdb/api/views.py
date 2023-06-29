from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework. filters import SearchFilter, OrderingFilter

from reviews.models import Category, Title, Genre
from .serializers import CategorySerializer, TitleSerializer, GenreSerializer
from .mixins import ListCreateDeleteViewSet


class CategoryViewSet(ListCreateDeleteViewSet):
    """ВьюСет для котегорий."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDeleteViewSet):
    """ВьюСет для жанров."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """ВьюСет для произведений."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ('category', 'genre', 'name', 'year')
