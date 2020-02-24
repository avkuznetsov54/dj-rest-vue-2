from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class IsMortgageEditorOrAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(dir(request))
        # print(request.user.groups.all())
        if view.action == 'list':
            return bool(request.user and request.user.is_authenticated)
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Редактор Ипотека'))
        else:
            return False
            # return Response(status=status.HTTP_404_NOT_FOUND)
            # raise PermissionDenied({"message": "You don't have permission to access"})
