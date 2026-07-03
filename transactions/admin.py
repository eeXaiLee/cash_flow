from typing import Any

from django.contrib import admin

from .models import Operation


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'status',
        'operation_type',
        'category',
        'subcategory',
        'amount',
        'short_description',
    )

    list_filter = (
        'status',
        'operation_type',
        'category',
        'subcategory',
        ('date', admin.DateFieldListFilter),
    )

    search_fields = (
        'comment',
        'category__name',
        'subcategory__name',
        'operation_type__name',
    )

    date_hierarchy = 'date'

    list_select_related = (
        'status',
        'operation_type',
        'category',
        'subcategory',
    )

    ordering = ('-date',)

    @admin.display(description='Описание')
    def short_description(self, obj: Any) -> str:
        return (
            f'{obj.status.name} | {obj.category.name} → {obj.subcategory.name}'
        )
