from rest_framework.permissions import BasePermission, SAFE_METHODS


class BasePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user == obj.user or request.user.is_staff:
            return True
        else:
            return False