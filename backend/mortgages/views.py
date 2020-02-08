from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import MortgagePrograms, Banks, TargetCredits
from .serializers import MortgageProgramsSerializer, BanksSerializer, TargetCreditsSerializer


class MortgagePagination(PageNumberPagination):
    page_size = 1000


class MortgageProgramsView(generics.ListAPIView):
    serializer_class = MortgageProgramsSerializer
    queryset = MortgagePrograms.objects.all()
    pagination_class = MortgagePagination
    permission_classes = (IsAuthenticated, )

    def filter_queryset(self, queryset):
        for k, v in self.request.query_params.items():
            params = {}
            # if k == "cursor":
            #     continue

            # если 'v' равно пустой строке то прекращаем итерацию что не занести её в queryset, а то 500 error
            if v == '':
                continue
            if k == 'bank_name':
                k = 'programs_bank__bank_name' + '__in'
                v = v.split(',')
                params.update({k: v})
            if k == 'names_target_credits':
                k = 'programs_target__target_name' + '__in'
                v = v.split(',')
                params.update({k: v})
            if k == 'property_value':
                k1 = 'min_sum_credit' + '__lte'
                params.update({k1: v})
                k2 = 'max_sum_credit' + '__gte'
                params.update({k2: v})
            if k == 'rate':
                k = k + '__lte'
                params.update({k: v})
            if k == 'first_payment':
                k = k + '__lte'
                params.update({k: v})
            queryset = queryset.filter(**params)
            # тоже самое что:
            # queryset = queryset.filter(model__icontains="asdf")

        # return queryset.order_by('-rate')
        return queryset


# class BanksView(generics.ListAPIView):
#     serializer_class = BanksSerializer
#     queryset = Banks.objects.all()
#     permission_classes = (IsAuthenticated,)


class BankViewSet(ModelViewSet):
    serializer_class = BanksSerializer
    queryset = Banks.objects.all()
    permission_classes = (IsAuthenticated,)


# class TargetCreditsView(generics.ListAPIView):
#     serializer_class = TargetCreditsSerializer
#     queryset = TargetCredits.objects.all()
#     permission_classes = (IsAuthenticated,)


class TargetCreditsViewSet(ModelViewSet):
    serializer_class = TargetCreditsSerializer
    queryset = TargetCredits.objects.all()
    permission_classes = (IsAuthenticated,)
