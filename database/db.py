import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "smartspend.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def create_table():

    connection = get_connection()

    # Transactions table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # Monthly budgets table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),

            PRIMARY KEY (month, category)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
    print("SmartSpend database tables created successfully!")