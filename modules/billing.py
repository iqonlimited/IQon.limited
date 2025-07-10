import json
from datetime import datetime
import uuid
import os

DATA_FILE = "data/transactions.json"

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_transactions(transactions):
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

def add_transaction(user_email, amount, currency, plan, method, status="success"):
    transactions = load_transactions()
    transaction = {
        "id": str(uuid.uuid4()),
        "user_email": user_email,
        "amount": amount,
        "currency": currency,
        "plan": plan,
        "method": method,  # e.g. 'stripe', 'razorpay'
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions.append(transaction)
    save_transactions(transactions)
    return transaction

def get_user_transactions(user_email):
    transactions = load_transactions()
    return [t for t in transactions if t["user_email"] == user_email]

def get_all_transactions():
    return load_transactions()

def get_revenue_summary():
    transactions = load_transactions()
    summary = {}
    for t in transactions:
        if t["status"] != "success":
            continue
        key = f"{t['currency']}:{t['plan']}"
        summary[key] = summary.get(key, 0) + float(t["amount"])
    return summary
