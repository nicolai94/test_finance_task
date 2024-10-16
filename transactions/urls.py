from django.urls import path, include
from rest_framework.routers import DefaultRouter

from transactions.views import ReportView, ExportTransactionsCSV, BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet)
router.register(r"budgets", BudgetViewSet, basename="budget")

urlpatterns = [
    path("", include(router.urls)),
    path("report/", ReportView.as_view(), name="report"),
    path("export-transactions/", ExportTransactionsCSV.as_view(), name="export-transactions"),
]
