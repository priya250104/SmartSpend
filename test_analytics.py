
from services.analytics_service import (
    get_financial_metrics,
    get_category_expenses,
    get_monthly_summary
)

from storage import load_transactions


transactions = load_transactions()

print("\n========== FINANCIAL METRICS ==========")

metrics = get_financial_metrics(transactions)

for key, value in metrics.items():
    print(f"{key}: {value}")


print("\n========== CATEGORY EXPENSES ==========")

print(get_category_expenses(transactions))


print("\n========== MONTHLY SUMMARY ==========")

print(get_monthly_summary(transactions))
