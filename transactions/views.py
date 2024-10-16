import csv

from django.db import models
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Budget, Transaction
from transactions.serializers import BudgetSerializer, TransactionSerializer
from users.models import User


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class ReportView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        transactions = (
            Transaction.objects.filter(user=user, date__range=[start_date, end_date])
            .values("transaction_type")
            .annotate(total=models.Sum("amount"))
        )

        return Response(transactions, status=status.HTTP_200_OK)


class ExportTransactionsCSV(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(user=user)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Amount", "Date", "Type", "Category"])

        for transaction in transactions:
            writer.writerow(
                [transaction.id, transaction.amount, transaction.date, transaction.type, transaction.category]
            )

        return response
