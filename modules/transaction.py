import json
import os
import uuid
from datetime import datetime

TRANSACTION_FILE = "data/transactions.json"
WALLET_FILE = "data/wallets.json"

# --------------------- Utility Functions ---------------------

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --------------------- Wallet Functions ---------------------

def get_wallet(email):
    wallets = load_json(WALLET_FILE)
    for wallet in wallets:
        if wallet["email"].lower() == email.lower():
            return wallet
    return {"email": email, "balance": 0.0}

def update_wallet(email, amount):
    wallets = load_json(WALLET_FILE)
    for wallet in wallets:
        if wallet["email"].lower() == email.lower():
            wallet["balance"] += float(amount)
            save_json(WALLET_FILE, wallets)
            return wallet

    # If wallet doesn't exist
    new_wallet = {"email": email, "balance": float(amount)}
    wallets.append(new_wallet)
    save_json(WALLET_FILE, wallets)
    return new_wallet

def deduct_wallet(email, amount):
    wallets = load_json(WALLET_FILE)
    for wallet in wallets:
        if wallet["email"].lower() == email.lower():
            if wallet["balance"] >= float(amount):
                wallet["balance"] -= float(amount)
                save_json(WALLET_FILE, wallets)
                return True
            else:
                return False
    return False

# --------------------- Transaction Functions ---------------------

def record_transaction(email, txn_type, amount, description, source="manual", membership_plan=None):
    transactions = load_json(TRANSACTION_FILE)
    txn = {
        "id": str(uuid.uuid4()),
        "email": email,
        "type": txn_type,  # "membership", "ebook", "wallet_topup", etc.
        "amount": float(amount),
        "description": description,
        "membership_plan": membership_plan,
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions.append(txn)
    save_json(TRANSACTION_FILE, transactions)
    return txn

def get_user_transactions(email):
    transactions = load_json(TRANSACTION_FILE)
    return [txn for txn in transactions if txn["email"].lower() == email.lower()]

def get_all_transactions():
    return load_json(TRANSACTION_FILE)

def get_revenue_summary():
    transactions = load_json(TRANSACTION_FILE)
    total = sum(txn["amount"] for txn in transactions if txn["type"] in ["membership", "ebook"])
    return total
