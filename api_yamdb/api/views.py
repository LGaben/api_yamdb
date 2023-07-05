from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework import viewsets, status, views
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from reviews.filters import TitleFilterSet
from reviews.models import Category, Title, Genre, Review
from users.models import User
from .serializers import (
    CategorySerializer,
    TitleSerializer,
    GenreSerializer,
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleNotSafeMetodSerialaizer
)
from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdminOrReadOnly, IsAdmin


class CategoryViewSet(ListCreateDeleteViewSet):
    """ВьюСет для котегорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
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

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return TitleNotSafeMetodSerialaizer
        return TitleSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter)
    search_fields = ('=user__username')
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if self.request.method == 'PATCH':
                serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class SignUpViewSet(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data.get('username'),
                                    email=request.data.get('email')
                                    )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения : {confirmation_code}',
                settings.ADMIN_EMAIL,
                (user.email,),
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=request.data.get('username')
            )
            if not default_token_generator.check_token(
                user, request.data.get('confirmation_code')
            ):
                return Response(
                    'Неверный confirmation_code',
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
