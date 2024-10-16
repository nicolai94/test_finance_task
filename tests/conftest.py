import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    "tests.fixtures.user",
    "tests.fixtures.transaction",
]


@pytest.fixture
def client():
    yield APIClient()
