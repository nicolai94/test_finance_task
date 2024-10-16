from django.core.validators import EmailValidator
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
