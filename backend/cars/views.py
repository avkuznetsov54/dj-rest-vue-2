from django.shortcuts import render
from rest_framework import generics
from .serializers import CarDetailSerializer, CarListSerializer
from .models import Car
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.viewsets import ModelViewSet


class CarCreateView(generics.CreateAPIView):
    serializer_class = CarDetailSerializer


class CarListView(generics.ListAPIView):
    serializer_class = CarListSerializer
    queryset = Car.objects.all()
    permission_classes = (IsAuthenticated, )
    # permission_classes = (IsAdminUser, )


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAdminUser)


class MyPagination(CursorPagination):
    page_size = 15
    # page_size_query_param = 'page_size'
    # max_page_size = 15
    ordering = 'id'


class CarViewSet(ModelViewSet):
    serializer_class = CarListSerializer
    queryset = Car.objects.all()
    pagination_class = MyPagination

    def filter_queryset(self, queryset):
        for k, v in self.request.query_params.items():
            if k == "cursor":
                continue
            queryset = queryset.filter(**{k: v})
            # тоже самое что:
            # queryset = queryset.filter(model__icontains="asdf")
        return queryset
