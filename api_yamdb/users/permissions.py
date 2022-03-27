from rest_framework import permissions

class IsMe(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin

