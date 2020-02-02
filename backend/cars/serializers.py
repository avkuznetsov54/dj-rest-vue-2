from rest_framework import serializers
from .models import Car


class CarListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # вместо id выводиться username

    class Meta:
        model = Car
        fields = ('vin', 'color', 'brand', 'car_type', 'user', 'year', 'volume')
        # fields = '__all__'

    # вместо username_id выводиться username
    def get_user(self, obj):
        return obj.user.username


class CarDetailSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = '__all__'
