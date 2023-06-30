from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Title, Genre
from users.models import User


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализотор для категорий."""

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализоватор для жанров."""

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    username = serializers.CharField(read_only=True, max_length=20)
    email = serializers.EmailField(read_only=True, max_length=254)
    role = serializers.CharField(read_only=True)

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
    username = serializers.CharField(read_only=True, max_length=20)
    email = serializers.EmailField(read_only=True, max_length=254)

    class Meta:
        model = User
        fields = ('username',
                  'email')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]
    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(f'Логин {username} недоступен')
        return username


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для входа пользователя."""
    username = serializers.CharField(required=True, max_length=20)
    confirmation_code = serializers.SlugField(required=True)
    extra_kwargs = {
        'username': {'required': True},
        'confirmation_code': {'required': True}}
