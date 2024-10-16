import pytest

from users.models import User


@pytest.fixture
def user_fixture(db):
    user = User.objects.create_user(first_name="first_name", last_name="first_user", email="admin@mail.com")
    return user
