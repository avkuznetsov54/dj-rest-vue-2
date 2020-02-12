from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MortgageProgramsViewSet, BankViewSet, TargetCreditsViewSet


router = DefaultRouter()
router.register('banks', BankViewSet, basename='banks')
router.register('target-credits', TargetCreditsViewSet, basename='target-credits')
router.register('all', MortgageProgramsViewSet, basename='mortgage-program')

app_name = 'mortgages'
# urlpatterns = [
#     # path('all/', MortgageProgramsView.as_view()),
#     # path('banks/', BanksView.as_view()),
#     # path('target-credits/', TargetCreditsView.as_view()),
# ]

urlpatterns = router.urls
