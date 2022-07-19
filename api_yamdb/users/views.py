from django.contrib.auth import get_user_model
from rest_framework import filters, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .models import ROLE_ADMIN
from .permissions import IsAdmin
from .serializers import SingUpSerializer, TokenGetSerializer, UserSerializer


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenGetSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username']

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated, ),
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user

        if request.method == 'get':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        if request.data.get('role'):
            if user.role != ROLE_ADMIN and user.role != request.data['role']:
                raise serializers.ValidationError({
                    'error': 'Обычный пользователь не может менять свою роль',
                    'role': user.role,
                })

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
