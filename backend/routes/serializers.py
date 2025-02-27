from rest_framework import serializers
from .models import Route, RoutePhoto, Comment, CompletedRoute


class RoutePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePhoto
        fields = ['id', 'photo', 'uploaded_at']


class RouteSerializer(serializers.ModelSerializer):
    # Сериализуем точки маршрута (список координат)
    points = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),  # Широта и долгота
            allow_empty=False
        ),
        required=True
    )

    # Сериализуем фотографии маршрута
    photos = RoutePhotoSerializer(many=True, required=False)  # Фото могут быть не обязательными

    class Meta:
        model = Route
        fields = ['id', 'name', 'type', 'description', 'rating', 'points', 'users', 'published', 'photos']

    def create(self, validated_data):
        # Извлекаем фотографии из данных
        photos_data = validated_data.pop('photos', [])
        points_data = validated_data.pop('points', [])

        # Создаем маршрут
        route = Route.objects.create(**validated_data)

        # Сохраняем точки маршрута
        route.points = points_data
        route.save()

        # Сохраняем фотографии маршрута, если они есть
        for photo_data in photos_data:
            RoutePhoto.objects.create(route=route, **photo_data)

        return route


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Показываем имя автора комментария
    replies = serializers.SerializerMethodField()  # Для отображения ответов на комментарий

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'parent_comment', 'replies']

    def get_replies(self, obj):
        # Если комментарий имеет ответы, то возвращаем их
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def create(self, validated_data):
        # Создаем комментарий, если есть родительский комментарий, то это ответ
        parent_comment = validated_data.pop('parent_comment', None)
        comment = Comment.objects.create(**validated_data, parent_comment=parent_comment)
        return comment


class CompletedRouteSerializer(serializers.ModelSerializer):
    route_name = serializers.StringRelatedField(source='route.name')  # Получаем название маршрута
    user_email = serializers.StringRelatedField(source='user.email')  # Получаем email пользователя

    class Meta:
        model = CompletedRoute
        fields = ['id', 'route', 'route_name', 'user', 'user_email', 'rating', 'completed_at']