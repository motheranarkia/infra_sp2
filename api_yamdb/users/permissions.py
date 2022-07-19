from rest_framework import permissions

from .models import ROLE_ADMIN


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == ROLE_ADMIN or request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == ROLE_ADMIN or request.user.is_superuser:
            return True
        return False
