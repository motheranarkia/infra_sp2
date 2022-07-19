from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    UserViewSet,
)


router = DefaultRouter()
router.register('users', UserViewSet)

auth_url_patterns = [
    path(
        'signup/',
        CustomTokenObtainPairView.as_view(),
        name='Регистрация и получение кода подтверждения',
    ),
    path(
        'token/',
        CustomTokenRefreshView.as_view(),
        name='Получение токена',
    ),
]

urlpatterns = [
    path('v1/auth/', include(auth_url_patterns)),
    path('v1/', include(router.urls)),
]
