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


class UserInfoCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return User.objects.all()

    def post(self, request, *args, **kwargs):
        # получаем refresh_token с фронта
        if request.data:
            try:
                # print(request.GET)
                refresh_token = request.data.get('refresh_token')
                # определяем QuerySet
                refresh_token_in_db = OutstandingToken.objects.filter(token=refresh_token)
                # вытаскиваем user
                # print(refresh_token_in_db.get().user)
                # вытаскиваем все values
                # print(refresh_token_in_db.values())
                # ищем в модели User
                queryset = User.objects.filter(username=refresh_token_in_db.get().user)
                serializer = UserSerializer(queryset, many=True)
                # print(Response(serializer.data))
                # возвращаем объект username
                return Response(serializer.data)
            except:
                # print('неправельные токен')
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)
        # return Response(status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


class MyUserView(generics.RetrieveAPIView):
    """Вытаскиваем всех юзеров"""
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


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
