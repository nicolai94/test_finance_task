import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user(client):
    url = reverse("user-list")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.first().email == data["email"]


@pytest.mark.django_db
def test_get_user(client, user_fixture):
    url = reverse("user-detail", args=[user_fixture.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user_fixture.email


@pytest.mark.django_db
def test_update_user(client, user_fixture):
    url = reverse("user-detail", args=[user_fixture.id])
    data = {"first_name": "Updated", "last_name": "first_user_upd", "email": "admin@mail.com"}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user_fixture.refresh_from_db()
    assert user_fixture.first_name == "Updated"


@pytest.mark.django_db
def test_delete_user(client, user_fixture):
    url = reverse("user-detail", args=[user_fixture.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 0
