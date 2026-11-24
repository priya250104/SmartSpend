# 💰 SmartSpend – Personal Finance Tracker & Analytics Dashboard

SmartSpend is a Python-based personal finance management application that helps users track income, manage expenses, monitor monthly budgets, and analyze their financial activities through an interactive Streamlit dashboard.

The application uses SQLite for persistent data storage, Pandas for financial data processing, and Plotly for interactive visualizations.

## 🚀 Features

### 1. Transaction Management
- Add income and expense transactions.
- View transaction history.
- Search transactions using transaction IDs.
- Edit and delete existing transactions.
- Filter transactions by type, category, and date.
- Sort transactions by amount and date.
- Import existing transaction records from JSON.

### 2. Financial Analytics
- Calculate total income.
- Calculate total expenses.
- Monitor available balance.
- Calculate savings percentage.
- Analyze category-wise expenses.
- Generate monthly financial summaries.

### 3. Budget Management
- Create monthly budgets for expense categories.
- Update existing budgets.
- Track spending against allocated budgets.
- Calculate remaining budget and usage percentage.
- Generate alerts when spending reaches 80% or exceeds 100% of a budget.
- Delete saved budgets.

### 4. Interactive Dashboard
- Financial overview with key metrics.
- Date range filtering.
- Transaction type and category filters.
- Expense distribution donut chart.
- Monthly income vs. expenses chart.
- Monthly net savings trend.
- Top five spending categories.
- Category-wise budget progress.
- Budget alerts and transaction history.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| SQLite | Database management |
| Pandas | Financial data analysis |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| Git & GitHub | Version control and project hosting |

## 📁 Project Structure

```text
SmartSpend/
│
├── app.py
├── dashboard.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│