from rest_framework import permissions

from users.models import ROLE_ADMIN, ROLE_MODERATOR


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ разрешен автору объекта, модератору, администратору
    или только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if (
            request.user.role in (ROLE_ADMIN, ROLE_MODERATOR)
            or request.user.is_superuser
            or obj.author == request.user
        ):
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == ROLE_ADMIN or request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == ROLE_ADMIN or request.user.is_superuser:
            return True
        return False
