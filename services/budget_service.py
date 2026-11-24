
from database.db import get_connection, create_table
from datetime import datetime


# =====================================================
# SET OR UPDATE MONTHLY BUDGET
# =====================================================

def set_budget(category, amount, month=None):

    if amount <= 0:
        raise ValueError("Budget amount must be greater than zero.")

    if not category or not category.strip():
        raise ValueError("Category cannot be empty.")

    if month is None:
        month = datetime.today().strftime("%Y-%m")

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Month must be in YYYY-MM format.")

    create_table()

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO budgets (month, category, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(month, category)
            DO UPDATE SET amount = excluded.amount
        """, (month, category.strip(), float(amount)))

        connection.commit()

    finally:
        connection.close()


# =====================================================
# GET ALL BUDGETS FOR A MONTH
# =====================================================

def get_budgets(month=None):

    if month is None:
        month = datetime.today().strftime("%Y-%m")

    create_table()

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT month, category, amount
            FROM budgets
            WHERE month = ?
            ORDER BY category
        """, (month,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# =====================================================
# GET BUDGET SUMMARY
# =====================================================

def get_budget_summary(month=None):

    if month is None:
        month = datetime.today().strftime("%Y-%m")

    budgets = get_budgets(month)

    create_table()

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT category, COALESCE(SUM(amount), 0) AS spent
            FROM transactions
            WHERE type = 'Expense'
              AND substr(date, 1, 7) = ?
            GROUP BY category
        """, (month,))

        spending = {
            row["category"]: float(row["spent"])
            for row in cursor.fetchall()
        }

    finally:
        connection.close()

    summary = []

    for budget in budgets:

        category = budget["category"]
        budget_amount = float(budget["amount"])
        spent = spending.get(category, 0.0)

        remaining = budget_amount - spent

        usage_percentage = (
            (spent / budget_amount) * 100
            if budget_amount > 0 else 0
        )

        summary.append({
            "month": month,
            "category": category,
            "budget": round(budget_amount, 2),
            "spent": round(spent, 2),
            "remaining": round(remaining, 2),
            "usage_percentage": round(usage_percentage, 2)
        })

    return summary


# =====================================================
# DELETE MONTHLY BUDGET
# =====================================================

def delete_budget(category, month=None):

    if month is None:
        month = datetime.today().strftime("%Y-%m")

    create_table()

    connection = get_connection()

    try:
        cursor = connection.execute("""
            DELETE FROM budgets
            WHERE month = ? AND category = ?
        """, (month, category))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# =====================================================
# GENERATE BUDGET ALERTS
# =====================================================

def get_budget_alerts(month=None):

    summary = get_budget_summary(month)

    alerts = []

    for item in summary:

        category = item["category"]
        percentage = item["usage_percentage"]
        spent = item["spent"]
        budget = item["budget"]

        if percentage >= 100:

            alerts.append({
                "category": category,
                "level": "Exceeded",
                "message": (
                    f"{category} budget exceeded! "
                    f"Spent ₹{spent:,.2f} "
                    f"against ₹{budget:,.2f}."
                )
            })

        elif percentage >= 80:

            alerts.append({
                "category": category,
                "level": "Warning",
                "message": (
                    f"{category} budget is "
                    f"{percentage:.1f}% used. "
                    f"Only ₹{item['remaining']:,.2f} remaining."
                )
            })

    return alerts
