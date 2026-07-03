from drf_spectacular.utils import extend_schema
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from .filters import OperationFilter
from .models import Operation
from .serializers import OperationReadSerializer, OperationWriteSerializer


@extend_schema(tags=['Операции ДДС'])
class OperationViewSet(ModelViewSet):
    """
    Возвращает вложенные справочники при чтении
    и использует первичные ключи при записи.
    """
    queryset = (
        Operation.objects
        .select_related(
            'status',
            'operation_type',
            'category',
            'subcategory',
        )
    )
    filterset_class = OperationFilter

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action in ('list', 'retrieve'):
            return OperationReadSerializer
        return OperationWriteSerializer
