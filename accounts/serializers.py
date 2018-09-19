from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
    email = serializers.CharField()
    success = serializers.BooleanField(default=False)


class UserSerializer(serializers.ModelSerializer):
    user_check = UniqueValidator(
        queryset=User.objects.all(),
        message='Email already exists'
    )
    email = serializers.EmailField(
        required=True,
        validators=[user_check],
        style={'input_type': 'email', 'placeholder': 'Email',
               'autofocus': True}
    )
    username = serializers.CharField(
        style={'input_type': 'text', 'placeholder': 'username',
               'autofocus': True}
    )
    password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password', 'placeholder': 'password',
               'autofocus': True}
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()
