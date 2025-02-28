from django.urls import path
from . import views

urlpatterns = [
    # Путь для создания маршрута
    path('create_route/', views.create_route, name='create-route'),

    path('get_routes/', views.get_all_routes, name='get-all-routes'),
    path('get_route/<int:route_id>/', views.get_route, name='get-route'),

    path('get_unpublished_routes/', views.get_unpublished_routes, name='get-un-routes'),
    path('route/<int:route_id>/publish/', views.publish_route, name='publish-route'),

    # Путь для добавления комментария или ответа
    path('route/<int:route_id>/comment/', views.add_comment, name='add-comment'),

    # Путь для получения всех комментариев маршрута
    path('route/<int:route_id>/comments/', views.get_comments_for_route, name='get-comments-for-route'),

    # Путь для получения всех комментариев пользователя
    path('user/comments/', views.get_user_comments, name='get-user-comments'),

    # Путь для создания пройденного маршрута
    path('route/<int:route_id>/complete/', views.mark_route_as_completed, name='mark-route-as-completed'),

    # Путь для получения всех пройденных маршрутов пользователя
    path('user/completed_routes/', views.get_completed_routes_for_user, name='get-completed-routes-for-user'),
]
