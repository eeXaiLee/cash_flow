from rest_framework.viewsets import ModelViewSet

from .models import Category, OperationType, Status, Subcategory
from .serializers import (
    CategorySerializer,
    OperationTypeSerializer,
    StatusSerializer,
    SubcategorySerializer,
)


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.order_by('name', 'id')
    serializer_class = StatusSerializer


class OperationTypeViewSet(ModelViewSet):
    queryset = OperationType.objects.order_by('name', 'id')
    serializer_class = OperationTypeSerializer


class CategoryViewSet(ModelViewSet):
    queryset = (
        Category.objects
        .select_related('operation_type')
        .order_by('name', 'id')
    )
    serializer_class = CategorySerializer


class SubcategoryViewSet(ModelViewSet):
    queryset = (
        Subcategory.objects
        .select_related('category')
        .order_by('name', 'id')
    )
    serializer_class = SubcategorySerializer
