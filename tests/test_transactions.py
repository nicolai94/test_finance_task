import logging
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from transactions.models import Transaction

logger = logging.getLogger("main")


@pytest.mark.django_db
def test_create_transaction(client, user_fixture):
    url = "/api/transactions/"
    data = {
        "user": user_fixture.id,
        "amount": Decimal("100.0"),
        "transaction_type": "income",
        "category": "Salary",
        "date": "2024-10-14",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.count() == 1
    assert Transaction.objects.get().amount == Decimal(100)


@pytest.mark.django_db
def test_get_transaction(client, transaction_fixture):
    url = f"/api/transactions/{transaction_fixture.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == "100.00"


@pytest.mark.django_db
def test_update_transaction(client, transaction_fixture):
    url = f"/api/transactions/{transaction_fixture.id}/"
    data = {
        "user": transaction_fixture.user.id,
        "amount": 200.0,
        "transaction_type": "income",
        "category": "Salary",
        "date": "2024-10-14",
    }
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    transaction_fixture.refresh_from_db()
    assert transaction_fixture.amount == 200.0


@pytest.mark.django_db
def test_delete_transaction(client, transaction_fixture):
    url = f"/api/transactions/{transaction_fixture.id}/"
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_create_budget(client, user_fixture):
    url = reverse("budget-list")
    data = {
        "user": user_fixture.id,
        "category": "Food",
        "limit": 500.0,
        "start_date": "2024-10-01",
        "end_date": "2024-10-31",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_generate_report(client, user_fixture, transaction_fixture, transaction_fixture2):
    url = reverse("report")
    response = client.get(url, {"user_id": user_fixture.id, "start_date": "2024-10-01", "end_date": "2024-10-31"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
