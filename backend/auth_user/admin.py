from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .models import Mods, Subdivision, Office, JobPosition, UserProfile

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


class SubdivisionAdmin(admin.ModelAdmin):
    class Meta:
        model = Subdivision

    list_display = ('name', )
    ordering = ['name']


class OfficeAdmin(admin.ModelAdmin):
    class Meta:
        model = Office

    list_display = ('name', 'address', )
    ordering = ['name']


class JobPositionAdmin(admin.ModelAdmin):
    class Meta:
        model = JobPosition

    list_display = ('name', )
    ordering = ['name']


admin.site.register(Subdivision, SubdivisionAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(JobPosition, JobPositionAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username',
                    'email',
                    # 'first_name',
                    # 'last_name',
                    'is_staff',
                    # 'is_superuser',
                    'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        # (('Personal info'), {
        #     'fields': ('first_name', 'last_name', 'email')
        # }),
        (('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (('Important dates'), {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    list_editable = ['is_active']
    inlines = (UserProfileInline,)

    class Meta:
        model = User

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Если у пользователя есть доступ в админку запрещаем для него отображение суперпользователя
        return qs.filter(is_superuser=False)

    def get_readonly_fields(self, request, obj=None):
        # Запрещённые поля для редактирования для пользователя с доступом в админку
        return () if request.user.is_superuser else ('is_staff', 'is_superuser', 'groups', 'user_permissions')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
