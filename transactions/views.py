from rest_framework.viewsets import ModelViewSet

from .models import Operation
from .serializers import OperationReadSerializer, OperationWriteSerializer


class OperationViewSet(ModelViewSet):
    queryset = (
        Operation.objects
        .select_related(
            'status',
            'operation_type',
            'category',
            'subcategory',
        )
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OperationReadSerializer
        return OperationWriteSerializer
