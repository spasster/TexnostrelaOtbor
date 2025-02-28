from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'author', 'type', 'rating', 'published', 'created_at')  # Отображаемые колонки в списке
    list_filter = ('type', 'published', 'created_at')  # Фильтры справа
    search_fields = ('name', 'author__email')  # Поля для поиска
    ordering = ('-created_at',)  # Сортировка (по дате создания, сначала новые)
    raw_id_fields = ('author', 'users')  # Для удобного выбора пользователей

# Если не используешь @admin.register:
# admin.site.register(Route, RouteAdmin)
