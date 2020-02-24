from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions

from mortgages.permissions import IsMortgageEditorOrAuthenticatedReadOnly
from .models import MortgagePrograms, Banks, TargetCredits
from .serializers import MortgageProgramsSerializer, BanksSerializer, TargetCreditsSerializer, MortgageProgSer

import re


class MortgagePagination(PageNumberPagination):
    page_size = 1000


class MortgageProgramsView(generics.ListAPIView):
# class MortgageProgramsViewSet(ModelViewSet):
    serializer_class = MortgageProgramsSerializer
    queryset = MortgagePrograms.objects.all().select_related('programs_bank').prefetch_related('programs_target')
    pagination_class = MortgagePagination
    permission_classes = (IsAuthenticated, )
    # permission_classes = (IsMortgageEditorOrAuthenticatedReadOnly, )

    # # очищаем поле programs_target (many2many) перед тем как перезаписать
    # def update(self, request, *args, **kwargs):
    #     mort = self.get_object()
    #     mort.programs_target.clear()
    #     return super().update(request, *args, **kwargs)

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
                v = re.sub("\D", "", v)
                k1 = 'min_sum_credit' + '__lte'
                params.update({k1: v})
                k2 = 'max_sum_credit' + '__gte'
                params.update({k2: v})
            if k == 'rate':
                k = k + '__lte'
                params.update({k: v})
            if k == 'is_rate_salary':
                k1 = 'rate_salary' + '__gte'
                if v == 'yes':
                    v1 = 0
                    params.update({k1: v1})
                    print(k1, v1)
            if k == 'first_payment':
                k = k + '__lte'
                params.update({k: v})
            if k == 'borrower_age':
                k1 = 'min_borrower_age' + '__lte'
                params.update({k1: v})
                k2 = 'max_borrower_age' + '__gte'
                params.update({k2: v})
            if k == 'time_credit':
                k1 = 'min_time_credit' + '__lte'
                params.update({k1: v})
                k2 = 'max_time_credit' + '__gte'
                params.update({k2: v})
            if k == 'work_experience':
                k = k + '__lte'
                params.update({k: v})
            if k == 'understatement_is_active':
                if v == 'true':
                    params.update({k: True})
            if k == 'express_issue':
                params.update({k: v})
            if k == 'inclusion_children':
                if v != 'null':
                    params.update({k: v})
            queryset = queryset.filter(**params)
            # тоже самое что:
            # queryset = queryset.filter(model__icontains="asdf")

        return queryset.order_by('rate').distinct()
        # return queryset


class CRUDMortgageProgramsViewSet(ModelViewSet):
    serializer_class = MortgageProgramsSerializer
    queryset = MortgagePrograms.objects.all().select_related('programs_bank').prefetch_related('programs_target')
    # pagination_class = MortgagePagination
    # permission_classes = (IsAuthenticated, )
    permission_classes = (IsMortgageEditorOrAuthenticatedReadOnly, )

    # очищаем поле programs_target (many2many) перед тем как перезаписать
    def update(self, request, *args, **kwargs):
        mort = self.get_object()
        mort.programs_target.clear()
        return super().update(request, *args, **kwargs)


# class BanksView(generics.ListAPIView):
#     serializer_class = BanksSerializer
#     queryset = Banks.objects.all()
#     permission_classes = (IsAuthenticated,)


class BankViewSet(ModelViewSet):
    serializer_class = BanksSerializer
    queryset = Banks.objects.all()
    permission_classes = (IsMortgageEditorOrAuthenticatedReadOnly,)


# class TargetCreditsView(generics.ListAPIView):
#     serializer_class = TargetCreditsSerializer
#     queryset = TargetCredits.objects.all()
#     permission_classes = (IsAuthenticated,)


class TargetCreditsViewSet(ModelViewSet):
    serializer_class = TargetCreditsSerializer
    queryset = TargetCredits.objects.all()
    permission_classes = (IsMortgageEditorOrAuthenticatedReadOnly,)
