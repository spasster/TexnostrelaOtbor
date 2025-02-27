from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from .views import register_user, CustomAuth, ChangePasswordView, update_avatar

urlpatterns = [
    path('register/', register_user, name='auth_register'),
    path('login/', CustomAuth.as_view(), name='auth_login'),

    path('change_password/', ChangePasswordView.as_view(), name='auth_change'),
    path('change_avatar/', update_avatar, name='ava_change'),


    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]
