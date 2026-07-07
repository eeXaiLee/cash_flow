from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.test import APIClient

from references.models import Category, OperationType, Status, Subcategory
from transactions.models import Operation


@pytest.mark.django_db
def test_get_statuses(api_client: APIClient, status: Status) -> None:
    """Возвращает список статусов через API."""
    response = api_client.get(
        reverse('status-list')
    )

    assert response.status_code == http_status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['name'] == 'Бизнес'


@pytest.mark.django_db
def test_create_operation(
    api_client: APIClient,
    status: Status,
    operation_type: OperationType,
    category: Category,
    subcategory: Subcategory
) -> None:
    """Создаёт новую запись ДДС через POST-запрос."""
    response = api_client.post(
        reverse('operation-list'),
        {
            'status': status.id,
            'operation_type': operation_type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '1000',
        },
        format='json'
    )

    assert response.status_code == http_status.HTTP_201_CREATED
    assert Decimal(response.data['amount']) == Decimal('1000')


@pytest.mark.django_db
def test_create_operation_with_invalid_category(
    api_client: APIClient,
    status: Status,
    category: Category,
    subcategory: Subcategory
) -> None:
    """Возвращает ошибку при несоответствии категории типу операции."""
    income_type = OperationType.objects.create(
        name='Пополнение'
    )

    response = api_client.post(
        reverse('operation-list'),
        {
            'status': status.id,
            'operation_type': income_type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '1000',
        },
        format='json'
    )

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert 'category' in response.data


@pytest.mark.django_db
def test_filter_operations_by_status(
    api_client: APIClient,
    operation: Operation,
) -> None:
    """Фильтрует операции по идентификатору статуса."""

    response = api_client.get(
        reverse('operation-list'),
        {
            'status': operation.status.id,
        }
    )

    assert response.status_code == http_status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == operation.id
