from rest_framework import permissions


class IsActive(permissions.BasePermission):
    """Разрешает доступ только активным пользователям"""
    def has_permission(self, request, view):
        return request.user.is_active
