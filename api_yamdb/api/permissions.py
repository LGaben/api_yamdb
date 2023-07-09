from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

# В версии djangorestframework-3.14.0 данные пермишены проходят тесты
# На версии djangorestframework-3.12.4 отказывается ((
# поэтому оставили так. Правильно ли мы их сделали?
# После ревью комментарии удалю.


class IsOwnerAdminModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    message = 'Изменить контент может только автор.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author)

# class IsOwner(permissions.IsAuthenticatedOrReadOnly):
#     message = 'Изменить контент может только админ или модератор.'

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.user.is_authenticated
#             and request.user == obj.author)


# class ReadOnly(permissions.BasePermission):
#     message = 'Изменить контент может только админ или модератор.'

#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS


# class IsModerator(permissions.BasePermission):
#     message = 'Изменить контент может только админ или модератор.'

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
