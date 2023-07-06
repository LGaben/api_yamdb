from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Title, Genre, Review, Comment
from users.models import User
from .validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализотор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализоватор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleNotSafeMetodSerialaizer(serializers.ModelSerializer):
    """Сеализатор для создания, удаления и изменения произведения."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        model = Title
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category',)
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(required=True, max_length=150,
                                     validators=[validate_username, UnicodeUsernameValidator()]
                                     )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username',
                  'email')
    def validate_exist(self, attrs): 
        username = attrs.get('username') 
        if_user = User.objects.filter(username=username) 
        if if_user.exists(): 
            raise ValidationError('Пользователь с таким именем уже существует') 
        email = attrs.get('email') 
        if_email = User.objects.filter(email=email) 
        if if_email.exists(): 
            raise ValidationError('Почта уже использовалась') 


class TokenSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title, author=request.user).exists():
                raise ValidationError('Можно оставлять только один'
                                      'отзыв на произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'