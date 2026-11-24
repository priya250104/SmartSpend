
from database.db import get_connection, create_table
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "data" / "transactions.json"


def load_transactions():
    """Load transactions from SQLite database."""

    create_table()

    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, type, amount, category, description, date
        FROM transactions
        ORDER BY date DESC
    """)

    transactions = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return transactions


def save_transactions(transactions):
    """Save transactions into SQLite database."""

    create_table()

    connection = get_connection()

    try:
        connection.execute("BEGIN")

        connection.execute("DELETE FROM transactions")

        for transaction in transactions:
            connection.execute("""
                INSERT INTO transactions
                (id, type, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                transaction["id"],
                transaction["type"],
                transaction["amount"],
                transaction["category"],
                transaction["description"],
                transaction["date"]
            ))

        connection.commit()
        print("Transactions saved successfully in SQLite!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def import_json_transactions():
    """Import existing JSON transactions into SQLite once."""

    create_table()

    connection = get_connection()

    existing_count = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    connection.close()

    if existing_count > 0 or not JSON_FILE.exists():
        return

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            old_transactions = json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Could not read the existing JSON file.")
        return

    if old_transactions:
        save_transactions(old_transactions)
        print(
            f"Successfully imported {len(old_transactions)} "
            "transactions from JSON!"
        )
