from django.db import models

from config.constants import MAX_NAME_LENGTH


class Status(models.Model):
    """Статус операции."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        verbose_name='Название статуса'
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self) -> str:
        return self.name


class OperationType(models.Model):
    """Тип операции."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, unique=True, verbose_name='Название типа'
    )

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Категория операции."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название категории'
    )
    operation_type = models.ForeignKey(
        OperationType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'operation_type'),
                name='unique_category_per_operation_type',
            )
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.operation_type.name})'


class Subcategory(models.Model):
    """Подкатегория операции."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название подкатегории'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'category'),
                name='unique_subcategory_per_category',
            )
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.category.name})'
