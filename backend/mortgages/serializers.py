from rest_framework import serializers
from .models import Banks, MortgagePrograms, TargetCredits


class TargetCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCredits
        fields = ('id', 'target_name', 'target_desc')


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = ('id', 'bank_name', 'bank_logo', 'preference_is_active', 'preference_value', 'preference_comment')


class MortgageProgramsSerializer(serializers.ModelSerializer):
    # programs_bank = serializers.SerializerMethodField()

    # включаем данные из связанных моделей
    bank = BanksSerializer(source='programs_bank')
    targets = TargetCreditsSerializer(source='programs_target', many=True)

    # programs_target_id = serializers.PrimaryKeyRelatedField(many=True,
    #                                                         read_only=False,
    #                                                         queryset=TargetCredits.objects.all(),
    #                                                         source='programs_target')

    class Meta:
        model = MortgagePrograms
        fields = ('id',
                  'programs_bank',
                  'programs_target',
                  'programs_name',
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
                  'work_experience',
                  'mandatory_documents',
                  'proof_of_income_document',
                  'time_for_bank_decision',
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
                  'req_tech_docs',
                  'add_info'
                  )

    # def get_programs_bank(self, obj):
    #     return obj.programs_bank.bank_name

    def update(self, instance, validated_data):

        # переписываем метод, чтоб заработал метод patch с many2many field
        new_programs_target = validated_data.pop('programs_target')
        # чтоб записались остальные поля помимо many2many
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        # чтоб записалось поле many2many
        for group in new_programs_target:
            instance.programs_target.add(group)
        instance.save()

        return instance


    # def update(self, instance, validated_data):
    #     tags_data = validated_data.pop('programs_target')
    #     instance = super(MortgageProgramsSerializer, self).update(instance, validated_data)
    #
    #     for tag_data in tags_data:
    #         tag_qs = TargetCredits.objects.filter(id=tag_data['id'])
    #
    #         if tag_qs.exists():
    #             tag = tag_qs.first()
    #         else:
    #             tag = TargetCredits.objects.create(**tag_data)
    #
    #         instance.tag.add(tag)
    #
    #     return instance


class MortgageProgSer(serializers.ModelSerializer):
    class Meta:
        model = MortgagePrograms
        fields = ('programs_bank',
                  'programs_target',
                  'programs_name',
                  'rate',
                  'rate_salary',
                  'first_payment',
                  'min_sum_credit',
                  'max_sum_credit',
                  'min_time_credit',
                  'max_time_credit',
                  'min_borrower_age',
                  'max_borrower_age',
                  'work_experience',
                  'mandatory_documents',
                  'proof_of_income_document',
                  'time_for_bank_decision',
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
                  'req_tech_docs',
                  'add_info'
                  )
