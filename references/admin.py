from django.contrib import admin

from .models import Category, OperationType, Status, Subcategory


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'categories_count',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = (CategoryInline,)

    @admin.display(description='Категорий')
    def categories_count(self, obj: OperationType) -> int:
        return obj.categories.count()


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'operation_type', 'subcategories_count',)
    list_filter = ('operation_type',)
    search_fields = ('name', 'operation_type__name',)
    list_select_related = ('operation_type',)
    ordering = ('operation_type__name', 'name')
    inlines = (SubcategoryInline,)

    @admin.display(description='Подкатегорий')
    def subcategories_count(self, obj: Category) -> int:
        return obj.subcategories.count()


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)
    list_filter = ('category', 'category__operation_type',)
    search_fields = (
        'name',
        'category__name',
        'category__operation_type__name',
    )
    list_select_related = ('category',)
    ordering = ('category__operation_type__name', 'category__name', 'name')
