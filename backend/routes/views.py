from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
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


@api_view(['GET'])
def get_route(request, route_id):
    """
    Метод для получения опеределенного маршрутов.
    """
    route = Route.objects.get(published=True, id=route_id)  # Извлекаем все маршруты
    serializer = RouteSerializer(route)  # Сериализуем маршруты

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_unpublished_routes(request):
    """
    Метод для получения неопубликованных маршрутов.
    """
    routes = Route.objects.filter(published=False)  # Извлекаем все маршруты
    serializer = RouteSerializer(routes, many=True)  # Сериализуем маршруты

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Только аутентифицированные пользователи могут публиковать маршруты
def publish_route(request, route_id):
    """
    Метод для публикации маршрута. Меняет поле published на True.
    Доступ только для автора маршрута.
    """
    try:
        route = Route.objects.get(id=route_id)  # Получаем маршрут по ID
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    # Обновляем статус опубликованного маршрута
    route.published = True
    route.save()

    return Response({"message": "Route published successfully", "route": route.name}, status=status.HTTP_200_OK)


@api_view(['POST'])
def mark_route_as_completed(request, route_id):
    """
    Метод для пометки маршрута как пройденного и добавления оценки.
    После оценки пересчитывается общий рейтинг маршрута.
    """
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, что оценка передана
    rating = request.data.get('rating')
    if rating is None:
        return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Оценка должна быть в пределах 1-5
    if rating < 1 or rating > 5:
        return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

    # Создаем объект CompletedRoute
    completed_route = CompletedRoute.objects.create(
        route=route,
        user=request.user,
        rating=rating
    )

    # Обновляем рейтинг маршрута
    update_route_rating(route)

    # Сериализуем и возвращаем пройденный маршрут
    serializer = CompletedRouteSerializer(completed_route)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def update_route_rating(route):
    """
    Функция для пересчета среднего рейтинга маршрута.
    """
    completed_routes = route.completed_routes.all()  # Получаем все завершенные маршруты для этого маршрута
    total_rating = sum([completed_route.rating for completed_route in completed_routes])  # Суммируем все оценки
    count = completed_routes.count()  # Количество оценок

    if count > 0:
        average_rating = total_rating / count  # Средний рейтинг
        # Обновляем рейтинг маршрута
        route.rating = round(average_rating, 1)  # Округляем до одного знака после запятой
        route.save()


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
