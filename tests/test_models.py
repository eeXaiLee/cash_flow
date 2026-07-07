from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from references.models import Category, OperationType, Status, Subcategory
from transactions.models import Operation


@pytest.mark.django_db
def test_category_str(category: Category) -> None:
    """Категория отображается вместе с названием типа операции."""
    assert str(category) == 'Маркетинг (Списание)'


@pytest.mark.django_db
def test_invalid_category_validation(
    status: Status, category: Category, subcategory: Subcategory
) -> None:
    """Запрещает выбирать категорию другого типа операции."""
    income_type = OperationType.objects.create(name='Пополнение')

    operation = Operation(
        status=status,
        operation_type=income_type,
        category=category,
        subcategory=subcategory,
        amount=Decimal('1000')
    )

    with pytest.raises(ValidationError):
        operation.full_clean()


@pytest.mark.django_db
def test_invalid_subcategory_validation(
    status: Status, operation_type: OperationType, subcategory: Subcategory
) -> None:
    """Запрещает выбирать подкатегорию другой категории."""
    another_category = Category.objects.create(
        name='Инфраструктура',
        operation_type=operation_type,
    )

    operation = Operation(
        status=status,
        operation_type=operation_type,
        category=another_category,
        subcategory=subcategory,
        amount=Decimal('1000')
    )

    with pytest.raises(ValidationError):
        operation.full_clean()
