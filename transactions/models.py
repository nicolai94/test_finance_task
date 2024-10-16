from django.db import models

from users.models import User


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.limit}"


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

    def check_budget_limit(self):
        budgets = Budget.objects.filter(user=self.user, category=self.category)
        for budget in budgets:
            total_expenses = (
                Transaction.objects.filter(
                    user=self.user,
                    category=self.category,
                    transaction_type="expense",
                    date__range=[budget.start_date, budget.end_date],
                ).aggregate(models.Sum("amount"))["amount__sum"]
                or 0
            )
            if total_expenses + self.amount > budget.limit:
                # send some message for example in SMTP or tg_bot
                pass
