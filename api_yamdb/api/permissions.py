from rest_framework import permissions

ROLES = ['admin', 'moderator', 'user']


class OnlyAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        return False


class AdminUserModerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser or request.user.role in ROLES:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.is_superuser
        ):
            return True


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
                request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if (
                request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser
        ):
            return True


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
