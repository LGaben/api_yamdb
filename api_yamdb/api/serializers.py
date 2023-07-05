from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Title, Genre, Review, Comment
from users.models import User


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
    category = CategorySerializer(read_only=True)

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
    category = CategorySerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genre', 'category', )

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category',)
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    username = serializers.CharField(read_only=True, max_length=150)
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
        def validate_email_length(self, email):
                if len(email) > 254:
                    raise ValidationError(f'Длина почтового адреса должна быть не больше 254 символов')
                return email

class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

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
    def validate_email_length(self, email):
        if len(email) > 254:
            raise ValidationError(f'Длина почтового адреса должна быть не больше 254 символов')
        return email


class TokenSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя."""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)
    extra_kwargs = {
        'username': {'required': True},
        'confirmation_code': {'required': True}}


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
