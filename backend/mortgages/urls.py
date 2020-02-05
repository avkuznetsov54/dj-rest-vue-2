from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MortgageProgramsView, BankViewSet, TargetCreditsViewSet


router = DefaultRouter()
router.register('banks', BankViewSet, basename='banks')
router.register('target-credits', TargetCreditsViewSet, basename='target-credits')

app_name = 'mortgages'
urlpatterns = [
    path('all/', MortgageProgramsView.as_view()),
    # path('banks/', BanksView.as_view()),
    # path('target-credits/', TargetCreditsView.as_view()),
]

urlpatterns += router.urls
