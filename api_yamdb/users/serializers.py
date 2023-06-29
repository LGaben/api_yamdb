from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, max_length=150)
    email = serializers.EmailField(read_only=True, max_length=254)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, max_length=150)
    email = serializers.EmailField(read_only=True, max_length=254)

    class Meta:
        model = User
        fields = ('username',
                  'email')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.SlugField(required=True)
    extra_kwargs = {
        'username': {'required': True},
        'confirmation_code': {'required': True}}
