from rest_framework import permissions
from apps.user_service.models import Admin


class CustomAuthenticationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, Admin):
            return bool(request.user and request.user.user.is_authenticated)
        else:
            return False


class IsWarehouseStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            return user.role == "WAREHOUSE_STAFF" or user.role == "WAREHOUSE_OWNER"
        except Admin.DoesNotExist:
            return False
