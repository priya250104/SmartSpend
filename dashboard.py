
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
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SmartSpend | Premium Finance",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# PREMIUM FINTECH THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #0B0F0E;
    color: #F3F5F4;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #F3F5F4 !important;
    font-weight: 700 !important;
}

p, label, span {
    color: #B8C2BD;
}

section[data-testid="stSidebar"] {
    background-color: #111715;
    border-right: 1px solid #242C28;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F3F5F4 !important;
}

section[data-testid="stSidebar"] p {
    color: #A7B3AC;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #171F1B, #121715);
    border: 1px solid #27332D;
    padding: 22px 20px;
    border-radius: 18px;
    transition: 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: #20C997;
    transform: translateY(-2px);
}

div[data-testid="stMetricLabel"] {
    color: #A7B3AC !important;
}

div[data-testid="stMetricValue"] {
    color: #F3F5F4 !important;
    font-weight: 700;
}

.stButton button,
.stFormSubmitButton button {
    background: #20C997;
    color: #07110D;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.55rem 1.1rem;
    transition: 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #36DDAA;
    color: #07110D;
    border: none;
}

button[kind="secondary"] {
    background: #1A2420 !important;
    color: #D7E0DA !important;
    border: 1px solid #2D3933 !important;
}

div[data-baseweb="input"],
div[data-baseweb="select"],
div[data-baseweb="textarea"] {
    background-color: #151B18;
}

input, textarea {
    color: #F3F5F4 !important;
}

div[data-baseweb="select"] > div {
    background-color: #151B18;
    border-color: #2B3630;
    border-radius: 10px;
}

div[data-testid="stDateInput"] input {
    background-color: #151B18;
    border: 1px solid #2B3630;
    border-radius: 10px;
}

button[data-baseweb="tab"] {
    color: #A7B3AC !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #20C997 !important;
    border-bottom-color: #20C997 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #27332D;
    border-radius: 12px;
    overflow: hidden;
}

div[data-testid="stProgressBar"] > div > div {
    background-color: #20C997;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #27332D;
}

.dashboard-header {
    background: linear-gradient(
        135deg,
        #17231D 0%,
        #111715 50%,
        #0F1814 100%
    );
    border: 1px solid #26352D;
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 25px;
}

.dashboard-title {
    font-size: 32px;
    font-weight: 800;
    color: #F3F5F4;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 15px;
    color: #9BAAA1;
    margin-bottom: 0;
}

.dashboard-badge {
    display: inline-block;
    background: #15382B;
    color: #42D99A;
    padding: 7px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid #23533F;
}

.section-label {
    color: #20C997;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.budget-card {
    background: #151B18;
    border: 1px solid #27332D;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}

.smartspend-footer {
    text-align: center;
    color: #69766E;
    font-size: 12px;
    padding: 25px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">💎 SmartSpend</div>
    <div class="dashboard-subtitle">
        Personal Finance & Analytics Dashboard
    </div>
    <br>
    <span class="dashboard-badge">
        ✦ PREMIUM FINANCIAL OVERVIEW
    </span>
</div>
""", unsafe_allow_html=True)


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
# LOAD DATA
# =====================================================

transactions = load_transactions()

if transactions is None:
    transactions = []


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("""
<div style="padding:10px 0 20px 0;">
    <h2 style="color:#20C997;margin-bottom:0;">
        💎 SmartSpend
    </h2>
    <p style="color:#7F8E85;font-size:13px;">
        Financial control center
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🔎 Filters")

filtered_transactions = []

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

        st.sidebar.markdown("**Date Range**")

        selected_dates = st.sidebar.date_input(
            "Select dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed"
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

    st.sidebar.markdown("**Transaction Type**")

    selected_type = st.sidebar.selectbox(
        "Type",
        ["All", "Income", "Expense"],
        label_visibility="collapsed"
    )

    available_categories = sorted(
        filter_df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    st.sidebar.markdown("**Category**")

    selected_category = st.sidebar.selectbox(
        "Category",
        ["All"] + available_categories,
        label_visibility="collapsed"
    )

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

    st.sidebar.info("No transactions yet.")
    start_date = None
    end_date = None

st.sidebar.divider()

st.sidebar.markdown("""
<div style="background:#151B18;border:1px solid #27332D;
border-radius:12px;padding:15px;">
    <div style="color:#20C997;font-weight:700;">
        💡 Smart Tip
    </div>
    <div style="color:#9BAAA1;font-size:13px;margin-top:5px;">
        Track your spending regularly to make smarter financial decisions.
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# DASHBOARD TABS
# =====================================================

tab_overview, tab_budget, tab_transactions, tab_add = st.tabs([
    "📊 Overview",
    "💰 Budgets",
    "📋 Transactions",
    "➕ Add Transaction"
])


# =====================================================
# OVERVIEW TAB
# =====================================================

with tab_overview:

    st.markdown(
        '<div class="section-label">Financial Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Your financial snapshot")

    if filtered_transactions:

        metrics = get_financial_metrics(
            filtered_transactions
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total Income",
            f"₹{metrics['total_income']:,.2f}"
        )

        col2.metric(
            "💸 Total Expenses",
            f"₹{metrics['total_expenses']:,.2f}"
        )

        col3.metric(
            "🏦 Available Balance",
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

    st.markdown("---")

    category_expenses = get_category_expenses(
        filtered_transactions
    )

    monthly_summary = get_monthly_summary(
        filtered_transactions
    )

    st.markdown("## Spending analytics")

    chart_col1, chart_col2 = st.columns(2)

    # Expense distribution

    with chart_col1:

        st.markdown("### Expense Distribution")

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
                hole=0.65,
                color_discrete_sequence=[
                    "#20C997",
                    "#36DDAA",
                    "#4F8F70",
                    "#A5D6B7",
                    "#F4B860",
                    "#FF817F",
                    "#8E7CFF",
                    "#57B8FF",
                    "#E78AC3",
                    "#B0BEC5"
                ]
            )

            fig_donut.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(
                    line=dict(
                        color="#111715",
                        width=3
                    )
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Amount: ₹%{value:,.2f}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                )
            )

            fig_donut.update_layout(
                height=400,
                paper_bgcolor="#0B0F0E",
                plot_bgcolor="#0B0F0E",
                font=dict(color="#DCE5DF"),
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#B8C2BD")
                ),
                margin=dict(l=10, r=10, t=20, b=20)
            )

            st.plotly_chart(
                fig_donut,
                width="stretch"
            )

        else:
            st.info("No expense records available.")

    # Monthly income vs expenses

    with chart_col2:

        st.markdown("### Monthly Income vs Expenses")

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
                color_discrete_sequence=[
                    "#20C997",
                    "#FF817F"
                ]
            )

            fig_monthly.update_layout(
                height=400,
                paper_bgcolor="#0B0F0E",
                plot_bgcolor="#151B18",
                font=dict(color="#DCE5DF"),
                xaxis=dict(
                    title="Month",
                    gridcolor="#27332D"
                ),
                yaxis=dict(
                    title="Amount (₹)",
                    gridcolor="#27332D"
                ),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10, r=10, t=20, b=20)
            )

            st.plotly_chart(
                fig_monthly,
                width="stretch"
            )

        else:
            st.info("No monthly financial data available.")

    st.markdown("---")

    chart_col3, chart_col4 = st.columns(2)

    # Savings trend

    with chart_col3:

        st.markdown("### Monthly Savings Trend")

        if not monthly_summary.empty:

            savings_df = monthly_summary.reset_index()

            savings_df["month"] = (
                savings_df["month"].astype(str)
            )

            fig_savings = px.line(
                savings_df,
                x="month",
                y="Balance",
                markers=True
            )

            fig_savings.update_traces(
                line=dict(color="#20C997", width=3),
                marker=dict(size=9, color="#20C997"),
                hovertemplate=(
                    "Month: %{x}<br>"
                    "Savings: ₹%{y:,.2f}"
                    "<extra></extra>"
                )
            )

            fig_savings.update_layout(
                height=400,
                paper_bgcolor="#0B0F0E",
                plot_bgcolor="#151B18",
                font=dict(color="#DCE5DF"),
                xaxis=dict(
                    title="Month",
                    gridcolor="#27332D"
                ),
                yaxis=dict(
                    title="Net Savings (₹)",
                    gridcolor="#27332D"
                ),
                margin=dict(l=10, r=10, t=20, b=20)
            )

            st.plotly_chart(
                fig_savings,
                width="stretch"
            )

        else:
            st.info("No savings trend available.")

    # Top spending categories

    with chart_col4:

        st.markdown("### Top 5 Spending Categories")

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
                color="Amount",
                color_continuous_scale=[
                    "#173E2E",
                    "#20C997"
                ]
            )

            fig_top.update_layout(
                height=400,
                paper_bgcolor="#0B0F0E",
                plot_bgcolor="#151B18",
                font=dict(color="#DCE5DF"),
                xaxis=dict(
                    title="Spending (₹)",
                    gridcolor="#27332D"
                ),
                yaxis=dict(
                    categoryorder="total ascending",
                    gridcolor="#27332D"
                ),
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=20, b=20)
            )

            st.plotly_chart(
                fig_top,
                width="stretch"
            )

        else:
            st.info("No spending categories available.")


# =====================================================
# BUDGET TAB
# =====================================================

with tab_budget:

    st.markdown(
        '<div class="section-label">Budget Management</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Take control of your spending")

    st.caption(
        "Set monthly limits, monitor category spending and receive budget alerts."
    )

    selected_budget_month = st.date_input(
        "Select Budget Month",
        value=date.today().replace(day=1),
        key="budget_month"
    )

    budget_month = selected_budget_month.strftime("%Y-%m")

    st.markdown("### Create or update a budget")

    with st.form("budget_form"):

        budget_category = st.selectbox(
            "Expense Category",
            expense_categories
        )

        budget_amount = st.number_input(
            "Monthly Budget (₹)",
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

    st.markdown("---")

    st.markdown("### Monthly Budget Summary")

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
            "💰 Total Budget",
            f"₹{total_budget:,.2f}"
        )

        col2.metric(
            "💸 Total Spent",
            f"₹{total_spent:,.2f}"
        )

        col3.metric(
            "🟢 Remaining",
            f"₹{total_remaining:,.2f}"
        )

        col4.metric(
            "📊 Utilization",
            f"{total_usage:.1f}%"
        )

        st.markdown("### Category Budget Tracking")

        for item in budget_summary:

            category = item["category"]
            budget = item["budget"]
            spent = item["spent"]
            remaining = item["remaining"]
            percentage = item["usage_percentage"]

            st.markdown(
                f"""
                <div class="budget-card">
                    <h4 style="color:#F3F5F4;margin-bottom:5px;">
                        {category}
                    </h4>
                    <p style="color:#9BAAA1;margin-bottom:0;">
                        Budget ₹{budget:,.2f}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(max(percentage / 100, 0.0), 1.0)
            )

            col1, col2, col3 = st.columns(3)

            col1.caption(f"Spent: ₹{spent:,.2f}")
            col2.caption(f"Remaining: ₹{remaining:,.2f}")
            col3.caption(f"Usage: {percentage:.1f}%")

            if percentage >= 100:
                st.error(f"🚨 {category} budget exceeded!")

            elif percentage >= 80:
                st.warning(
                    f"⚠️ {category} budget is nearly exhausted!"
                )

            else:
                st.success(
                    f"✓ {category} spending is within budget."
                )

            st.markdown("---")

    else:

        st.info(
            "No budgets found for this month. "
            "Create your first budget above."
        )

    # Budget alerts

    st.markdown("### 🔔 Budget Alerts")

    budget_alerts = get_budget_alerts(
        budget_month
    )

    if budget_alerts:

        for alert in budget_alerts:

            if alert["level"] == "Exceeded":
                st.error(alert["message"])
            else:
                st.warning(alert["message"])

    else:
        st.success(
            "No budget alerts. Your spending is under control!"
        )

    # Delete budget

    st.markdown("### Manage Budgets")

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
            "🗑️ Delete Selected Budget",
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
                st.error("Budget could not be deleted.")

    else:
        st.info("No saved budgets available for this month.")


# =====================================================
# TRANSACTIONS TAB
# =====================================================

with tab_transactions:

    st.markdown(
        '<div class="section-label">Transaction History</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Your transactions")

    if filtered_transactions:

        transaction_df = pd.DataFrame(
            filtered_transactions
        )

        # Add a fallback for older transactions that
        # were saved before the user_name field existed.
        if "user_name" not in transaction_df.columns:
            transaction_df["user_name"] = "Not provided"
        else:
            transaction_df["user_name"] = (
                transaction_df["user_name"]
                .fillna("Not provided")
                .astype(str)
            )

        transaction_df["amount"] = (
            transaction_df["amount"].astype(float)
        )

        if "date" in transaction_df.columns:
            transaction_df["date"] = pd.to_datetime(
                transaction_df["date"],
                errors="coerce"
            ).dt.date

        # Hide UUID and show the user's name instead.
        transaction_df = transaction_df.drop(
            columns=["id"],
            errors="ignore"
        )

        transaction_df = transaction_df.rename(
            columns={
                "user_name": "User Name",
                "type": "Type",
                "amount": "Amount (₹)",
                "category": "Category",
                "description": "Description",
                "date": "Date"
            }
        )

        # Put the user name first in the table.
        display_columns = [
            "User Name",
            "Type",
            "Amount (₹)",
            "Category",
            "Description",
            "Date"
        ]

        display_columns = [
            column
            for column in display_columns
            if column in transaction_df.columns
        ]

        transaction_df = transaction_df[display_columns]

        st.dataframe(
            transaction_df,
            width="stretch",
            hide_index=True
        )

        st.caption(
            f"Showing {len(filtered_transactions)} transactions"
        )

    else:

        st.info(
            "No transactions found for the selected filters."
        )


# =====================================================
# ADD TRANSACTION TAB
# =====================================================

with tab_add:

    st.markdown(
        '<div class="section-label">New Transaction</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Add income or expense")

    st.caption(
        "Enter your transaction details below."
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"],
        key="new_transaction_type"
    )

    categories = (
        income_categories
        if transaction_type == "Income"
        else expense_categories
    )

    with st.form("transaction_form"):

        # NEW: User Name field
        user_name = st.text_input(
            "User Name",
            placeholder="Enter your name"
        )

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

            if not user_name.strip():

                st.error("Please enter the user's name.")

            else:

                new_transaction = {
                    "id": str(uuid4()).upper(),

                    # NEW: Save user's name
                    "user_name": user_name.strip(),

                    "type": transaction_type,
                    "amount": float(amount),
                    "category": category,
                    "description": description,
                    "date": transaction_date.isoformat()
                }

                transactions.append(new_transaction)

                save_transactions(transactions)

                st.success(
                    f"Transaction added successfully for {user_name.strip()}!"
                )

                st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="smartspend-footer">
    SmartSpend Premium · Personal Finance Analytics
    <br>
    Built with Python · SQLite · Pandas · Streamlit · Plotly
</div>
""", unsafe_allow_html=True)
