from rest_framework import viewsets, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from reviews.models import Category, Title, Genre, Review
from users.models import CustomUser

from .serializers import (CategorySerializer,
                         TitleSerializer,
                         GenreSerializer,
                         UserSerializer,
                         SignUpSerializer,
                         TokenSerializer,
                         ReviewSerializer,
                         CommentSerializer)
from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdminOrReadOnly, IsAdmin


class CategoryViewSet(ListCreateDeleteViewSet):
    """ВьюСет для котегорий."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['pk'])
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ListCreateDeleteViewSet):
    """ВьюСет для жанров."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs['pk'])
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(ModelViewSet):
    """ВьюСет для произведений."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ('category', 'genre', 'name', 'year')


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter)
    search_fields = ('=user__username')


class SignUpViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    pass


class TokenViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,)

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