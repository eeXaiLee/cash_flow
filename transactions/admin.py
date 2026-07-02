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
        'comment'
    )
    list_filter = (
        'status',
        'operation_type',
        'category',
        'subcategory',
        'date'
    )
    search_fields = ('comment',)
    date_hierarchy = 'date'
    list_select_related = (
        'status',
        'operation_type',
        'category',
        'subcategory'
    )
