from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from references.models import Category, OperationType, Status, Subcategory
from transactions.models import Operation


@pytest.fixture
def api_client() -> APIClient:
    """Клиент DRF для выполнения HTTP-запросов к API."""
    return APIClient()


@pytest.fixture
def status() -> Status:
    """Статус «Бизнес» для операций ДДС."""
    return Status.objects.create(name='Бизнес')


@pytest.fixture
def operation_type() -> OperationType:
    """Тип операции «Списание»."""
    return OperationType.objects.create(name='Списание')


@pytest.fixture
def category(operation_type: OperationType) -> Category:
    """Категория «Маркетинг» для типа «Списание»."""
    return Category.objects.create(
        name='Маркетинг',
        operation_type=operation_type
    )


@pytest.fixture
def subcategory(category: Category) -> Subcategory:
    """Подкатегория «Avito» для категории «Маркетинг»."""
    return Subcategory.objects.create(
        name='Avito',
        category=category
    )


@pytest.fixture
def operation(
    status: Status,
    operation_type: OperationType,
    category: Category,
    subcategory: Subcategory
) -> Operation:
    """Операция списания на сумму 1500 рублей."""
    return Operation.objects.create(
        status=status,
        operation_type=operation_type,
        category=category,
        subcategory=subcategory,
        amount=Decimal('1500'),
        comment='Тестовая операция'
    )
