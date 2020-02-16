from rest_framework import permissions


class IsMortgageEditorOrAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(dir(request))
        # print(request.user.groups.all())
        # if view.action == 'list':
        #     return bool(request.user and request.user.is_authenticated)
        if view.action in ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='Редактор Ипотека'))
        else:
            return False
