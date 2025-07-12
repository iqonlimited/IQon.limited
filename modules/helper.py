import hashlib
import json
import os
from datetime import datetime
import uuid

# ---------------------- JSON Utils ----------------------
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------------- Auth ----------------------
def authenticate_user(email, password, user_data_file='data/users.json'):
    import json, os
    if not os.path.exists(user_data_file):
        return None
    with open(user_data_file, 'r', encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user.get("role")  # Return role directly
    return None

# ---------------------- Password Utils ----------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash

# ---------------------- Date & Time ----------------------
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def days_between(start_date, end_date):
    fmt = "%Y-%m-%d"
    return (datetime.strptime(end_date, fmt) - datetime.strptime(start_date, fmt)).days

# ---------------------- Unique Generators ----------------------
def generate_id():
    return str(uuid.uuid4())

def generate_transaction_id():
    return "TXN-" + str(uuid.uuid4())[:8].upper()

# ---------------------- General Utils ----------------------
def format_currency(amount, currency="$"):
    return f"{currency}{amount:,.2f}"

def truncate_text(text, max_length=50):
    return (text[:max_length] + "...") if len(text) > max_length else text
