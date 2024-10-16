import datetime
from decimal import Decimal

import pytest

from transactions.models import Transaction


@pytest.fixture
def transaction_fixture(db, user_fixture):
    transaction = Transaction.objects.create(
        user=user_fixture,
        amount=Decimal("100.00"),
        date=datetime.date(2024, 10, 14),
        transaction_type="income",
        category="test",
    )

    return transaction


@pytest.fixture
def transaction_fixture2(db, user_fixture):
    transaction = Transaction.objects.create(
        user=user_fixture,
        amount=Decimal("200.00"),
        date=datetime.date(2024, 10, 14),
        transaction_type="income",
        category="test2",
    )
    transaction.save()

    return transaction
