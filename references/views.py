from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from .models import Category, OperationType, Status, Subcategory
from .serializers import (
    CategorySerializer,
    OperationTypeSerializer,
    StatusSerializer,
    SubcategorySerializer,
)


@extend_schema(tags=['Статусы'])
class StatusViewSet(ModelViewSet):
    queryset = Status.objects.order_by('name')
    serializer_class = StatusSerializer


@extend_schema(tags=['Типы операций'])
class OperationTypeViewSet(ModelViewSet):
    queryset = OperationType.objects.order_by('name')
    serializer_class = OperationTypeSerializer


@extend_schema(tags=['Категории'])
class CategoryViewSet(ModelViewSet):
    queryset = (
        Category.objects
        .select_related('operation_type')
        .order_by('name')
    )
    serializer_class = CategorySerializer
    filterset_fields = ('operation_type',)


@extend_schema(tags=['Подкатегории'])
class SubcategoryViewSet(ModelViewSet):
    queryset = (
        Subcategory.objects
        .select_related('category')
        .order_by('name')
    )
    serializer_class = SubcategorySerializer
    filterset_fields = ('category',)
