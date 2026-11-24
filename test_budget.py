
from services.budget_service import (
    set_budget,
    get_budgets,
    get_budget_summary,
    get_budget_alerts,
    delete_budget
)

print("\n========== SET MONTHLY BUDGET ==========")

set_budget("Food", 5000)
set_budget("Shopping", 3000)
set_budget("Transport", 2000)

print("Budgets saved successfully!")


print("\n========== SAVED BUDGETS ==========")

print(get_budgets())


print("\n========== BUDGET SUMMARY ==========")

summary = get_budget_summary()

for item in summary:
    print(item)


print("\n========== BUDGET ALERTS ==========")

alerts = get_budget_alerts()

if alerts:
    for alert in alerts:
        print(alert["message"])
else:
    print("No budget alerts. Good spending!")


# Uncomment this section only when you want
# to test budget deletion.

# print(delete_budget("Food"))
