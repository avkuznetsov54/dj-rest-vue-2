from rest_framework import serializers
from .models import Banks, MortgagePrograms, TargetCredits


class TargetCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCredits
        fields = ('target_name', 'target_desc')


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = ('bank_name', 'bank_logo', 'preference_is_active', 'preference_value', 'preference_comment')


class MortgageProgramsSerializer(serializers.ModelSerializer):
    # programs_bank = serializers.SerializerMethodField()

    # включаем данные из связанных моделей
    bank = BanksSerializer(source='programs_bank')
    targets = TargetCreditsSerializer(source='programs_target', many=True)

    class Meta:
        model = MortgagePrograms
        fields = ('programs_name',
                  'bank',
                  'targets',
                  'rate',
                  'rate_salary',
                  'first_payment',
                  'min_sum_credit',
                  'max_sum_credit',
                  'min_time_credit',
                  'max_time_credit',
                  'min_borrower_age',
                  'max_borrower_age',
                  'understatement_is_active',
                  'understatement_comment',
                  'co_borrowers',
                  'commission',
                  'seller_registration',
                  'express_issue',
                  'inclusion_children',
                  'room',
                  'room_comment',
                  'share',
                  'share_comment',
                  'private_house',
                  'private_comment',
                  'apartments',
                  'apartments_comment',
                  'redevelopment',
                  'redevelopment_comment',
                  'overlap',
                  'storeys',
                  'housing_wear',
                  'req_tech_docs'
                  )

    # def get_programs_bank(self, obj):
    #     return obj.programs_bank.bank_name
