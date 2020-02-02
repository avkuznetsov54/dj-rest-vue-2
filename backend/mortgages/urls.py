from django.urls import path, include

from .views import MortgageProgramsView, BanksView, TargetCreditsView

app_name = 'mortgages'
urlpatterns = [
    path('all/', MortgageProgramsView.as_view()),
    path('banks/', BanksView.as_view()),
    path('target-credits/', TargetCreditsView.as_view()),
]
