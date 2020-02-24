from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Mods, UserProfile

from django.utils.translation import ugettext as _
from django.contrib.auth.models import update_last_login


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomJWTSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        """Обновляем поле last_login"""
        self.user.last_login = timezone.now()
        self.user.save()

        return RefreshToken.for_user(user)

    def validate(self, attrs):
        """делаем проверки при логине"""
        credentials = {
            # 'username': '',
            'username': attrs.get("username"),
            'password': attrs.get("password")
        }

        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        # user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        # if user_obj:
        #     credentials['username'] = user_obj.username

        # self.user.last_login = timezone.now()
        # self.user.save()

        # username = attrs.get("username")
        # if username is not None:
        #     domain_mail = username.split('@')[1]
        #     if domain_mail == 'bgnsk.ru':
        #         credentials['username'] = username
        #     else:
        #         msg = _('Почта не является корпоративной!')
        #         raise serializers.ValidationError(msg)

        # Default code
        data = super().validate(credentials)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        # Возвращаем на фронт username и groups
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        # print(dir(self.user))
        return data


# class UserInfoSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#
#         # Add extra responses here
#         data['username'] = self.user.username
#         data['groups'] = self.user.groups.values_list('name', flat=True)
#         return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserProfileSerializer(serializers.ModelSerializer):
    office = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('full_name', 'phone_number', 'subdivision', 'office', 'job_position', )

    def get_office(self, obj):
        return obj.office.name


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'groups', 'userprofile', )
        # fields = '__all__'

    # https://stackoverflow.com/questions/47691718/django-creating-a-custom-user-with-the-django-rest-framework
    # def create(self, validated_data, instance=None):
    #     profile_data = validated_data.pop('userprofile')
    #     user = User.objects.create(**validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     UserProfile.objects.update_or_create(user=user, **profile_data)
    #     return user


class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mods
        fields = '__all__'
