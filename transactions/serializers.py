from rest_framework import serializers

from transactions.models import Transaction, Budget


class TransactionSerializer(serializers.ModelSerializer):
    def validate_amount(self, value):
        if float(value) <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    class Meta:
        model = Transaction
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date")
        return data

    class Meta:
        model = Budget
        fields = "__all__"
