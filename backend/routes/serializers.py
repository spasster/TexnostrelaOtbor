from rest_framework import serializers
from .models import Route, RoutePhoto, Comment, CompletedRoute, RoutePoint


class RoutePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePhoto
        fields = ['id', 'photo', 'uploaded_at']


class RoutePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'photo', 'order']


class RouteSerializer(serializers.ModelSerializer):
    points = RoutePointSerializer(many=True, read_only=False)  # Сделаем точки редактируемыми
    photos = RoutePhotoSerializer(many=True, required=False)

    class Meta:
        model = Route
        fields = ['id', 'name', 'type', 'description', 'rating', 'points', 'users', 'published', 'photos']

    def create(self, validated_data):
        # Извлекаем фотографии и точки
        photos_data = validated_data.pop('photos', [])
        points_data = validated_data.pop('points', [])

        # Создаем маршрут
        route = Route.objects.create(**validated_data)

        # Сохраняем точки маршрута
        for point_data in points_data:
            # Убедимся, что поле `route` связано с созданным маршрутом
            RoutePoint.objects.create(route=route, **point_data)

        # Сохраняем фотографии маршрута
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