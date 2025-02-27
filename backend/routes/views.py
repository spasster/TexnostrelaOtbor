from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Route, RoutePhoto, Comment, CompletedRoute
from .serializers import RouteSerializer, CommentSerializer, CompletedRouteSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RouteSerializer


@api_view(['POST'])
def create_route(request):
    """
    Метод для создания нового маршрута с точками и фотографиями.
    """
    user = request.user  # Получаем текущего аутентифицированного пользователя

    serializer = RouteSerializer(data=request.data)

    if serializer.is_valid():
        route = serializer.save(author=user)  # Сохраняем маршрут

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_routes(request):
    """
    Метод для получения всех маршрутов.
    """
    routes = Route.objects.filter(published=True)  # Извлекаем все маршруты
    serializer = RouteSerializer(routes, many=True)  # Сериализуем маршруты

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def mark_route_as_completed(request, route_id):
    """
    Метод для пометки маршрута как пройденного и добавления оценки.
    """
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, что оценка передана
    rating = request.data.get('rating')
    if rating is None:
        return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Создаем объект CompletedRoute
    completed_route = CompletedRoute.objects.create(
        route=route,
        user=request.user,
        rating=rating
    )

    # Сериализуем и возвращаем пройденный маршрут
    serializer = CompletedRouteSerializer(completed_route)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_completed_routes_for_user(request):
    """
    Метод для получения всех пройденных маршрутов для текущего пользователя.
    """
    completed_routes = CompletedRoute.objects.filter(user=request.user)
    serializer = CompletedRouteSerializer(completed_routes, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_comment(request, route_id):
    """
    Метод для добавления комментария (или ответа) к маршруту.
    """
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    # Получаем текст комментария и родительский комментарий (если есть)
    text = request.data.get('text')
    parent_comment_id = request.data.get('parent_comment', None)

    if not text:
        return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Если это ответ, находим родительский комментарий
    parent_comment = None
    if parent_comment_id:
        try:
            parent_comment = Comment.objects.get(id=parent_comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Parent comment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Создаем комментарий
    comment = Comment.objects.create(
        route=route,
        author=request.user,
        text=text,
        parent_comment=parent_comment
    )

    # Сериализуем и возвращаем комментарий
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comments_for_route(request, route_id):
    """
    Метод для получения всех комментариев и ответов для маршрута.
    """
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(route=route, parent_comment=None)  # Получаем только корневые комментарии
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_comments(request):
    """
    Метод для получения всех комментариев и ответов текущего пользователя.
    """
    user_comments = Comment.objects.filter(author=request.user)
    serializer = CommentSerializer(user_comments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
