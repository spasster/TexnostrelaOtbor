from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'avatar': {'required': False},  # Аватар может быть не обязателен на старте
        }

    def create(self, validated_data):
        # Создание пользователя через менеджер
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            avatar=validated_data.get('avatar')  # Можно указать значение по умолчанию для аватара
        )
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                # Если аутентификация не удалась, ищем пользователя по email
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.email, password=password)
            except User.DoesNotExist:
                print(1)
                raise AuthenticationFailed('Invalid email or password.')

            if not user:
                print(2)
                raise AuthenticationFailed('Invalid email or password.')

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        return attrs

    def get_token(self, user):
        # Генерация токенов для пользователя
        return RefreshToken.for_user(user)
