from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from django.conf import settings

from .models import User
from .serializers import UserRegistrationSerializer, CustomAuthTokenSerializer, UserSerializer


@api_view(['POST'])
def register_user(request):
    """Регистрация пользователя с генерацией токенов."""
    # Сериализация данных запроса
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        # Создаем пользователя
        user = serializer.save()

        # Генерация refresh и access токенов
        refresh = RefreshToken.for_user(user)

        # Формируем ответ с токенами
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuth(TokenObtainPairView):
    """Кастомная авторизация с email и password"""

    authentication_classes = []
    permission_classes = [AllowAny]

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = serializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Только аутентифицированные пользователи могут видеть эту информацию
def get_user_info(request):
    """
    Метод для получения всей информации о текущем пользователе и всех его маршрутах.
    """
    user = request.user  # Получаем текущего аутентифицированного пользователя
    serializer = UserSerializer(user)  # Сериализуем пользователя с его маршрутами

    return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Позволяет аутентифицированному пользователю изменить свой пароль.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Пароль введен неверно."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"success": "Пароль успешно изменен."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_avatar(request):
    """
    Метод для обновления аватара пользователя.
    Загружает новый аватар и сохраняет его.
    """
    user = request.user  # Получаем текущего аутентифицированного пользователя

    # Проверяем, что файл был передан
    if 'avatar' not in request.FILES:
        return Response({"error": "No avatar file provided."}, status=status.HTTP_400_BAD_REQUEST)

    avatar_file = request.FILES['avatar']

    # Обновляем аватар пользователя
    user.avatar = avatar_file
    user.save()

    return Response({"message": "Avatar updated successfully."}, status=status.HTTP_200_OK)