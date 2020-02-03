from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)
from .views import ModsView, MyUserView, CustomTokenObtainPairView

from .views import Logout

urlpatterns = [
    # Path to obtain a new access and refresh token
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Submit your refresh token to this path to obtain a new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/logout/', Logout.as_view()),


    # Return 'Mods' model objects
    path('mods/', ModsView.as_view(), name='mods_view'),

    path('users', MyUserView.as_view()),

]
