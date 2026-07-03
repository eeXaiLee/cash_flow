import django_filters

from .models import Operation


class OperationFilter(django_filters.FilterSet):
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
            'date_from',
            'date_to',
            'status',
            'operation_type',
            'category',
            'subcategory',
        )
