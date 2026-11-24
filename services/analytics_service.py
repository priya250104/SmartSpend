import pandas as pd


def create_dataframe(transactions):
    """Convert transaction records into a Pandas DataFrame."""

    if not transactions:
        return pd.DataFrame(
            columns=[
                "id", "type", "amount",
                "category", "description", "date"
            ]
        )

    df = pd.DataFrame(transactions)

    df["amount"] = pd.to_numeric(
        df["amount"], errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    return df.dropna(subset=["amount", "date"])


def get_financial_metrics(transactions):
    """Calculate important financial metrics."""

    df = create_dataframe(transactions)

    income = df.loc[
        df["type"] == "Income", "amount"
    ].sum()

    expenses = df.loc[
        df["type"] == "Expense", "amount"
    ].sum()

    balance = income - expenses

    savings_rate = (
        (balance / income) * 100 if income > 0 else 0
    )

    return {
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "balance": round(balance, 2),
        "savings_rate": round(savings_rate, 2)
    }


def get_category_expenses(transactions):
    """Calculate expenses for each category."""

    df = create_dataframe(transactions)

    expenses = df[df["type"] == "Expense"]

    if expenses.empty:
        return pd.Series(dtype="float64")

    return (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )


def get_monthly_summary(transactions):
    """Calculate monthly income and expenses."""

    df = create_dataframe(transactions)

    if df.empty:
        return pd.DataFrame(
            columns=["Income", "Expenses", "Balance"]
        )

    df["month"] = df["date"].dt.to_period("M")

    monthly = df.pivot_table(
        index="month",
        columns="type",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    for column in ["Income", "Expense"]:
        if column not in monthly.columns:
            monthly[column] = 0

    monthly = monthly.rename(
        columns={"Expense": "Expenses"}
    )

    monthly["Balance"] = (
        monthly["Income"] - monthly["Expenses"]
    )

    return monthly[
        ["Income", "Expenses", "Balance"]
    ].round(2)
