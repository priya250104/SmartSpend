
import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date
from uuid import uuid4

from storage import load_transactions, save_transactions

from services.analytics_service import (
    get_financial_metrics,
    get_category_expenses,
    get_monthly_summary
)

from services.budget_service import (
    set_budget,
    get_budget_summary,
    get_budget_alerts,
    get_budgets,
    delete_budget
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SmartSpend | Finance Dashboard",
    page_icon="💰",
    layout="wide"
)


# =====================================================
# HEADER
# =====================================================

st.title("💰 SmartSpend")
st.subheader("Personal Finance Dashboard")

st.caption(
    "Manage your income, expenses, savings, and budgets "
    "with intelligent financial analytics."
)

st.divider()


# =====================================================
# CATEGORY LISTS
# =====================================================

income_categories = [
    "Salary",
    "Freelance",
    "Business",
    "Pocket Money",
    "Investment",
    "Other"
]

expense_categories = [
    "Food",
    "Rent",
    "Groceries",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Healthcare",
    "Entertainment",
    "Travel",
    "Other"
]


# =====================================================
# LOAD TRANSACTIONS
# =====================================================

transactions = load_transactions()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("🔎 Dashboard Filters")

if transactions:

    filter_df = pd.DataFrame(transactions)

    filter_df["date"] = pd.to_datetime(
        filter_df["date"],
        errors="coerce"
    )

    valid_dates = filter_df["date"].dropna()

    if not valid_dates.empty:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        st.sidebar.subheader("Date Range")

        selected_dates = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if (
            isinstance(selected_dates, (tuple, list))
            and len(selected_dates) == 2
        ):

            start_date, end_date = selected_dates

        else:

            start_date = min_date
            end_date = max_date

    else:

        start_date = None
        end_date = None

    st.sidebar.subheader("Transaction Type")

    selected_type = st.sidebar.selectbox(
        "Select type",
        ["All", "Income", "Expense"]
    )

    available_categories = sorted(
        filter_df["category"].dropna().unique().tolist()
    )

    st.sidebar.subheader("Category")

    selected_category = st.sidebar.selectbox(
        "Select category",
        ["All"] + available_categories
    )

    # Apply filters

    filtered_transactions = []

    for transaction in transactions:

        transaction_date = pd.to_datetime(
            transaction["date"],
            errors="coerce"
        )

        if start_date is not None and end_date is not None:

            if pd.isna(transaction_date):
                continue

            if not (
                start_date
                <= transaction_date.date()
                <= end_date
            ):
                continue

        if (
            selected_type != "All"
            and transaction["type"] != selected_type
        ):
            continue

        if (
            selected_category != "All"
            and transaction["category"] != selected_category
        ):
            continue

        filtered_transactions.append(transaction)

else:

    filtered_transactions = []


# =====================================================
# FINANCIAL METRICS
# =====================================================

st.header("📊 Financial Overview")

if filtered_transactions:

    metrics = get_financial_metrics(
        filtered_transactions
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Total Income",
        f"₹{metrics['total_income']:,.2f}"
    )

    col2.metric(
        "💸 Total Expenses",
        f"₹{metrics['total_expenses']:,.2f}"
    )

    col3.metric(
        "🏦 Balance",
        f"₹{metrics['balance']:,.2f}"
    )

    col4.metric(
        "📈 Savings Rate",
        f"{metrics['savings_rate']:.2f}%"
    )

else:

    st.info(
        "No transactions available for the selected filters."
    )


st.divider()


# =====================================================
# EXPENSE DISTRIBUTION
# =====================================================

st.header("🍩 Expense Distribution")

category_expenses = get_category_expenses(
    filtered_transactions
)

if not category_expenses.empty:

    expense_df = category_expenses.reset_index()

    expense_df.columns = [
        "Category",
        "Amount"
    ]

    fig_donut = px.pie(
        expense_df,
        names="Category",
        values="Amount",
        hole=0.55,
        title="Where Your Money Goes"
    )

    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Amount: ₹%{value:,.2f}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    fig_donut.update_layout(
        height=450,
        legend_title="Expense Categories"
    )

    st.plotly_chart(
        fig_donut,
        width="stretch"
    )

else:

    st.info("No expense records available.")


st.divider()


# =====================================================
# MONTHLY INCOME VS EXPENSES
# =====================================================

st.header("📊 Monthly Income vs Expenses")

monthly_summary = get_monthly_summary(
    filtered_transactions
)

if not monthly_summary.empty:

    monthly_display = monthly_summary.reset_index()

    monthly_display["month"] = (
        monthly_display["month"].astype(str)
    )

    fig_monthly = px.bar(
        monthly_display,
        x="month",
        y=["Income", "Expenses"],
        barmode="group",
        title="Monthly Income and Expenses",
        labels={
            "month": "Month",
            "value": "Amount (₹)",
            "variable": "Transaction Type"
        },
        color_discrete_sequence=[
            "#22C55E",
            "#EF4444"
        ]
    )

    fig_monthly.update_layout(
        height=450,
        xaxis_title="Month",
        yaxis_title="Amount (₹)"
    )

    st.plotly_chart(
        fig_monthly,
        width="stretch"
    )

else:

    st.info("No monthly financial data available.")


st.divider()


# =====================================================
# MONTHLY SAVINGS TREND
# =====================================================

st.header("📈 Monthly Net Savings Trend")

if not monthly_summary.empty:

    savings_df = monthly_summary.reset_index()

    savings_df["month"] = (
        savings_df["month"].astype(str)
    )

    fig_savings = px.line(
        savings_df,
        x="month",
        y="Balance",
        markers=True,
        title="Monthly Net Savings",
        labels={
            "month": "Month",
            "Balance": "Net Savings (₹)"
        }
    )

    fig_savings.update_traces(
        line_width=3,
        marker_size=8
    )

    fig_savings.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Net Savings (₹)"
    )

    st.plotly_chart(
        fig_savings,
        width="stretch"
    )

else:

    st.info("No savings trend available.")


st.divider()


# =====================================================
# TOP 5 SPENDING CATEGORIES
# =====================================================

st.header("🏆 Top 5 Spending Categories")

if not category_expenses.empty:

    top_categories = (
        category_expenses
        .head(5)
        .reset_index()
    )

    top_categories.columns = [
        "Category",
        "Amount"
    ]

    fig_top = px.bar(
        top_categories,
        x="Amount",
        y="Category",
        orientation="h",
        title="Highest Spending Categories",
        labels={
            "Amount": "Spending (₹)",
            "Category": "Category"
        },
        color="Amount",
        color_continuous_scale="Reds"
    )

    fig_top.update_layout(
        height=400,
        yaxis={
            "categoryorder": "total ascending"
        },
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_top,
        width="stretch"
    )

else:

    st.info("No spending categories available.")


st.divider()


# =====================================================
# PHASE 8: BUDGET MANAGEMENT
# =====================================================

st.header("💰 Budget Management")

st.write(
    "Set monthly spending limits and monitor your expenses."
)


# -----------------------------------------------------
# SELECT BUDGET MONTH
# -----------------------------------------------------

selected_budget_month = st.date_input(
    "Select Budget Month",
    value=date.today().replace(day=1),
    key="budget_month"
)

budget_month = selected_budget_month.strftime("%Y-%m")


# -----------------------------------------------------
# SET OR UPDATE BUDGET
# -----------------------------------------------------

st.subheader("➕ Set Monthly Category Budget")

with st.form("budget_form"):

    budget_category = st.selectbox(
        "Select Expense Category",
        expense_categories
    )

    budget_amount = st.number_input(
        "Monthly Budget Amount (₹)",
        min_value=1.0,
        value=5000.0,
        step=500.0
    )

    budget_submitted = st.form_submit_button(
        "💾 Save Budget",
        width="stretch"
    )

    if budget_submitted:

        try:

            set_budget(
                budget_category,
                budget_amount,
                budget_month
            )

            st.success(
                f"{budget_category} budget saved successfully!"
            )

            st.rerun()

        except ValueError as error:

            st.error(str(error))


# -----------------------------------------------------
# BUDGET SUMMARY
# -----------------------------------------------------

st.subheader("📊 Monthly Budget Summary")

budget_summary = get_budget_summary(
    budget_month
)

if budget_summary:

    total_budget = sum(
        item["budget"]
        for item in budget_summary
    )

    total_spent = sum(
        item["spent"]
        for item in budget_summary
    )

    total_remaining = total_budget - total_spent

    total_usage = (
        (total_spent / total_budget) * 100
        if total_budget > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Budget",
        f"₹{total_budget:,.2f}"
    )

    col2.metric(
        "Total Spent",
        f"₹{total_spent:,.2f}"
    )

    col3.metric(
        "Remaining",
        f"₹{total_remaining:,.2f}"
    )

    col4.metric(
        "Budget Used",
        f"{total_usage:.1f}%"
    )

    st.divider()

    # Category-wise budget progress

    st.subheader("📌 Category-wise Budget Tracking")

    for item in budget_summary:

        category = item["category"]
        budget = item["budget"]
        spent = item["spent"]
        remaining = item["remaining"]
        percentage = item["usage_percentage"]

        st.write(f"**{category}**")

        st.progress(
            min(max(percentage / 100, 0.0), 1.0)
        )

        col1, col2, col3 = st.columns(3)

        col1.caption(
            f"Budget: ₹{budget:,.2f}"
        )

        col2.caption(
            f"Spent: ₹{spent:,.2f}"
        )

        col3.caption(
            f"Remaining: ₹{remaining:,.2f}"
        )

        st.caption(
            f"Usage: {percentage:.1f}%"
        )

        if percentage >= 100:

            st.error(
                f"🚨 {category} budget exceeded!"
            )

        elif percentage >= 80:

            st.warning(
                f"⚠️ {category} budget is nearly exhausted!"
            )

        else:

            st.success(
                f"✅ {category} spending is within budget."
            )

        st.divider()

else:

    st.info(
        "No budgets found for this month. "
        "Set your first category budget above."
    )


# -----------------------------------------------------
# BUDGET ALERTS
# -----------------------------------------------------

st.subheader("🔔 Budget Alerts")

budget_alerts = get_budget_alerts(
    budget_month
)

if budget_alerts:

    for alert in budget_alerts:

        if alert["level"] == "Exceeded":

            st.error(
                alert["message"]
            )

        else:

            st.warning(
                alert["message"]
            )

else:

    st.success(
        "No budget alerts. Your spending is under control!"
    )


# -----------------------------------------------------
# DELETE BUDGET
# -----------------------------------------------------

st.subheader("🗑️ Manage Budgets")

saved_budgets = get_budgets(
    budget_month
)

if saved_budgets:

    budget_to_delete = st.selectbox(
        "Select budget to delete",
        [
            item["category"]
            for item in saved_budgets
        ],
        key="delete_budget_category"
    )

    if st.button(
        "Delete Selected Budget",
        type="secondary"
    ):

        deleted = delete_budget(
            budget_to_delete,
            budget_month
        )

        if deleted:

            st.success(
                f"{budget_to_delete} budget deleted successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Budget could not be deleted."
            )

else:

    st.info(
        "No saved budgets available for this month."
    )


st.divider()


# =====================================================
# TRANSACTION HISTORY
# =====================================================

st.header("📋 Transaction History")

if filtered_transactions:

    transaction_df = pd.DataFrame(
        filtered_transactions
    )

    transaction_df["amount"] = (
        transaction_df["amount"].astype(float)
    )

    st.dataframe(
        transaction_df,
        width="stretch",
        hide_index=True
    )

    st.caption(
        f"Showing {len(filtered_transactions)} transactions"
    )

else:

    st.info("No transactions found.")


st.divider()


# =====================================================
# ADD NEW TRANSACTION
# =====================================================

st.header("➕ Add New Transaction")

transaction_type = st.selectbox(
    "Transaction Type",
    ["Income", "Expense"],
    key="new_transaction_type"
)

if transaction_type == "Income":

    categories = income_categories

else:

    categories = expense_categories


with st.form("transaction_form"):

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        value=100.0,
        step=100.0
    )

    category = st.selectbox(
        "Category",
        categories
    )

    description = st.text_input(
        "Description",
        placeholder="Enter transaction details"
    )

    transaction_date = st.date_input(
        "Transaction Date",
        value=date.today(),
        max_value=date.today()
    )

    submitted = st.form_submit_button(
        "💾 Save Transaction",
        width="stretch"
    )

    if submitted:

        new_transaction = {
            "id": str(uuid4()).upper(),
            "type": transaction_type,
            "amount": float(amount),
            "category": category,
            "description": description,
            "date": transaction_date.isoformat()
        }

        transactions.append(new_transaction)

        save_transactions(transactions)

        st.success(
            "Transaction added successfully!"
        )

        st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "SmartSpend | Personal Finance Tracker | "
    "Python | SQLite | Pandas | Streamlit | Plotly"
)
