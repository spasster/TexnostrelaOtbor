from django.db import models
from django.contrib.auth import get_user_model


class Route(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default='private', choices=[('private', 'Private'), ('public', 'Public')])
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    users = models.ManyToManyField(get_user_model(), related_name='joined_routes', blank=True)
    published = models.BooleanField(default=False)

    # Поле для хранения точек маршрута (список координат)
    points = models.JSONField(default=list, blank=True, null=True)  # Храним список точек

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RoutePhoto(models.Model):
    route = models.ForeignKey(Route, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='routes_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for route {self.route.name}"


class Comment(models.Model):
    route = models.ForeignKey(Route, related_name='comments', on_delete=models.CASCADE)  # Связь с маршрутом
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')  # Связь с автором комментария
    text = models.TextField()  # Текст комментария
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # Родительский комментарий (если это ответ)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания комментария

    def __str__(self):
        return f"Comment by {self.author} on {self.route.name}"


class CompletedRoute(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='completed_routes')  # Связь с маршрутом
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='completed_routes')  # Связь с пользователем
    rating = models.IntegerField(default=0)  # Оценка маршрута, поставленная пользователем
    completed_at = models.DateTimeField(auto_now_add=True)  # Время, когда маршрут был завершен

    def __str__(self):
        return f"CompletedRoute by {self.user.email} on {self.route.name}"

