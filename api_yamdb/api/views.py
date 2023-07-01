from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerAdminModeratorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework. filters import SearchFilter, OrderingFilter

from reviews.models import Category, Title, Genre, Comment, Review
from .serializers import (CategorySerializer, TitleSerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer)
from .mixins import ListCreateDeleteViewSet


class CategoryViewSet(ListCreateDeleteViewSet):
    """ВьюСет для категорий."""

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get("review_id"),
            title__pk=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
