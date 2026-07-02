from django.core.exceptions import ValidationError
from django.db import models

from references.models import Category, OperationType, Status, Subcategory


class Operation(models.Model):
    date = models.DateField(
        verbose_name='Дата операции',
        help_text='Формат: ГГГГ-ММ-ДД'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='operations',
        verbose_name='Статус'
    )
    operation_type = models.ForeignKey(
        OperationType,
        on_delete=models.PROTECT,
        related_name='operations',
        verbose_name='Тип'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='operations',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='operations',
        verbose_name='Подкатегория'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма, руб.'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий'
    )

    class Meta:
        verbose_name = 'Операция ДДС'
        verbose_name_plural = 'Операции ДДС'
        ordering = ['-date']

    def __str__(self):
        return f'{self.date} - {self.operation_type.name} - {self.amount} руб.'

    def clean(self):
        """
        Проверяет бизнес-правила на уровне модели.

        Вызывается автоматически при сохранении через админку или
        при вызове full_clean().
        - Категория должна соответствовать выбранному типу операции.
        - Подкатегория должна принадлежать выбранной категории.
        """
        if not all([self.operation_type, self.category, self.subcategory]):
            return

        if self.category.operation_type != self.operation_type:
            raise ValidationError({
                'category':
                'Выбранная категория не относится к указанному типу операции.'
            })

        if self.subcategory.category != self.category:
            raise ValidationError({
                'subcategory':
                'Выбранная подкатегория не относится к указанной категории.'
            })
