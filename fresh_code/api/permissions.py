from rest_framework.permissions import BasePermission
from apps.users.models import User


class CustomAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN


# BasePermission
# class BasePermissionMetaclass(OperationHolderMixin, type):
#     pass
#
#
# class BasePermission(metaclass=BasePermissionMetaclass):
#     """
#     A base class from which all permission classes should inherit.
#     """
#
#     def has_permission(self, request, view):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True
