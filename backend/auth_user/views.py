from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .models import Mods
from django.contrib.auth.models import User
from .serializers import ModSerializer, UserSerializer, CustomJWTSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.models import update_last_login

from rest_framework import status
from rest_framework.views import APIView


class Logout(APIView):
    """Получаем refresh_token пользователя при логауте и удаляем его из БД"""
    def post(self, request):
        # print(request.data.get('refresh_token'))
        refresh_token = request.data.get('refresh_token')
        refresh_token_in_db = OutstandingToken.objects.filter(token=refresh_token)
        refresh_token_in_db.delete()

        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


# class UserInfoView(TokenObtainPairView):
#     serializer_class = UserInfoSerializer
#     # permission_classes = (IsAuthenticated,)


class MyUserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# class MyUserView2(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated, )
#
#     def filter_queryset(self, queryset):
#         queryset = queryset.filter(username=self.request.user)
#         return queryset


# View for 'Mods' model
class ModsView(generics.RetrieveAPIView):
    permission_classes = (IsAdminUser, )  # checks if user is authenticated to view the model objects
    # permission_classes = (IsAuthenticated, )  # checks if user is authenticated to view the model objects

    def get_queryset(self):
        return Mods.objects.all()  # return all model objects

    def get(self, request, *args, **kwargs):  # GET request handler for the model
        queryset = self.get_queryset()
        serializer = ModSerializer(queryset, many=True)
        return Response(serializer.data)
