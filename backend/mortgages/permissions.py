from rest_framework import permissions


class IsMortgageEditorOrAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(view.action)
        # print(request.user.groups.all())
        if view.action == 'list':
            return bool(request.user and request.user.is_authenticated)
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Редактор Ипотека'))
        else:
            return False
