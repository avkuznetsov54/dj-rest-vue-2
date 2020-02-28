from django.contrib import admin
from .models import Banks, MortgagePrograms, TargetCredits


class BanksAdmin(admin.ModelAdmin):
    class Meta:
        model = Banks

    list_display = ('bank_name', 'preference_is_active', 'preference_value', 'preference_comment')
    ordering = ['bank_name']


admin.site.register(Banks, BanksAdmin)


class TargetCreditsAdmin(admin.ModelAdmin):
    class Meta:
        model = TargetCredits

    list_display = ('target_name', 'target_desc')
    ordering = ['target_name']


admin.site.register(TargetCredits, TargetCreditsAdmin)


class MortgageProgramsAdmin(admin.ModelAdmin):
    class Meta:
        model = MortgagePrograms

    list_display = ('programs_bank', 'programs_name', 'rate', 'first_payment')
    ordering = ['programs_bank']
    readonly_fields = ['date_modified']


admin.site.register(MortgagePrograms, MortgageProgramsAdmin)
