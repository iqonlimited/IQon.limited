import json
import os
from datetime import datetime, timedelta

USER_FILE = "data/users.json"
WALLET_FILE = "data/wallets.json"

# Membership plans with monthly & yearly pricing
PLANS = {
    "basic": {"monthly": 4, "yearly": 40},
    "intermediate": {"monthly": 8, "yearly": 90},
    "ingenious": {"monthly": 14, "yearly": 120},
    "masters": {"monthly": 39, "yearly": 399},
    "students": {"monthly": 6},
}

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ------------------- Membership Core --------------------

def get_user_membership(email):
    users = load_json(USER_FILE)
    for user in users:
        if user["email"].lower() == email.lower():
            return user.get("membership", "guest")
    return "guest"

def update_membership(email, plan, duration="monthly"):
    users = load_json(USER_FILE)
    updated = False
    for user in users:
        if user["email"].lower() == email.lower():
            user["membership"] = plan
            user["membership_expiry"] = (
                (datetime.now() + timedelta(days=30 if duration == "monthly" else 365))
                .strftime("%Y-%m-%d")
            )
            updated = True
            break
    if updated:
        save_json(USER_FILE, users)
    return updated

# ------------------- Wallet Logic --------------------

def deduct_wallet(email, amount):
    wallets = load_json(WALLET_FILE)
    wallet = wallets.get(email, {"balance": 0})
    if wallet["balance"] >= amount:
        wallet["balance"] -= amount
        wallets[email] = wallet
        save_json(WALLET_FILE, wallets)
        return True
    return False

def add_to_wallet(email, amount):
    wallets = load_json(WALLET_FILE)
    wallet = wallets.get(email, {"balance": 0})
    wallet["balance"] += amount
    wallets[email] = wallet
    save_json(WALLET_FILE, wallets)
    return True

def get_wallet_balance(email):
    wallets = load_json(WALLET_FILE)
    return wallets.get(email, {}).get("balance", 0)

# ------------------- Access Control --------------------

def is_allowed_feature(email, required_plan):
    plan_order = ["guest", "basic", "intermediate", "ingenious", "masters", "students"]
    user_plan = get_user_membership(email)
    return plan_order.index(user_plan) >= plan_order.index(required_plan)

def get_available_plans():
    return PLANS