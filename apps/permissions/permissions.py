from .base_permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = 'User not authenticated'
    code = 'NoAuth'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsManager(BasePermission):
    """
    Allows access only to boss users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsMyTarget(BasePermission):
    """
    Allows access only to my targets
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True
        return obj.hitmen_by == request.user


class IsMyHit(BasePermission):
    """
    Allows access only to my hits
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True
        return obj.managed_by == request.user


class IsMyHitmen(BasePermission):
    """
    Allows access only to my hits
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True
        return obj.managed_by == request.user
