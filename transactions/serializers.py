from typing import Any

from rest_framework import serializers

from references.serializers import (
    CategorySerializer,
    OperationTypeSerializer,
    StatusSerializer,
    SubcategorySerializer,
)

from .models import Operation


class OperationReadSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    operation_type = OperationTypeSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)

    class Meta:
        model = Operation
        fields = (
            'id',
            'date',
            'status',
            'operation_type',
            'category',
            'subcategory',
            'amount',
            'comment',
        )


class OperationWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = (
            'id',
            'date',
            'status',
            'operation_type',
            'category',
            'subcategory',
            'amount',
            'comment',
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        operation_type = attrs.get('operation_type')
        category = attrs.get('category')
        subcategory = attrs.get('subcategory')

        if (
            operation_type
            and category
            and category.operation_type != operation_type
        ):
            raise serializers.ValidationError({
                'category':
                'Выбранная категория не относится к указанному типу операции.'
            })

        if (
            category
            and subcategory
            and subcategory.category != category
        ):
            raise serializers.ValidationError({
                'subcategory':
                'Выбранная подкатегория не относится к указанной категории.'
            })

        return attrs
