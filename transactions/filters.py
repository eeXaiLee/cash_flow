import django_filters

from .models import Operation


class OperationFilter(django_filters.FilterSet):
    """Фильтрация операций по диапазону дат и справочников."""
    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
    )
    date_to = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte'
    )

    class Meta:
        model = Operation
        fields = (
            'status',
            'operation_type',
            'category',
            'subcategory',
        )
