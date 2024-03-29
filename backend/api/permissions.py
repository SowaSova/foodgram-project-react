from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
)


class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ("GET",)
            or (request.user == obj.author)
            or request.user.is_staff
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ("GET",)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class OwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ("GET",)
            or (request.user == obj)
            or request.user.is_admin
        )


class AuthenticatedAndNotAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_anonymous
