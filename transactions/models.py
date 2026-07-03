from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from config.constants import (
    AMOUNT_DECIMAL_PLACES,
    AMOUNT_MAX_DIGITS,
    AMOUNT_MIN_VALUE,
)
from references.models import Category, OperationType, Status, Subcategory


class Operation(models.Model):
    date = models.DateField(
        default=timezone.localdate,
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
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        validators=[MinValueValidator(Decimal(AMOUNT_MIN_VALUE))],
        verbose_name='Сумма, руб.'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    class Meta:
        verbose_name = 'Операция ДДС'
        verbose_name_plural = 'Операции ДДС'
        ordering = ['-date']

    def __str__(self) -> str:
        return (
            f'{self.date} | '
            f'{self.operation_type} | '
            f'{self.category} | '
            f'{self.amount} ₽'
        )

    def clean(self) -> None:
        """
        Проверяет бизнес-правила на уровне модели.

        Вызывается автоматически при сохранении через админку или
        при вызове full_clean().
        - Категория должна соответствовать выбранному типу операции.
        - Подкатегория должна принадлежать выбранной категории.
        """
        if (
            self.operation_type is None
            or self.category is None
            or self.subcategory is None
        ):
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

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
