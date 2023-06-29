from rest_framework import serializers

from reviews.models import Category, Title, Genre

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

    genre = GenreSerializer(many=True, required=True, read_only=True)
    category = CategorySerializer(required=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
