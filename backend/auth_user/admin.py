from django.contrib import admin

# Register your models here.
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .models import Mods

admin.site.register(Mods)


class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):

    # def get_readonly_fields(self, *args, **kwargs):
    #     return True
    #
    # def has_add_permission(self, *args, **kwargs):
    #     return True

    def has_delete_permission(self, *args, **kwargs):
        return True

    # def has_change_permission(self, request, obj=None):
    #     return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)
