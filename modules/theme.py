import json
import os
import hashlib
import uuid
from datetime import datetime

USER_FILE = "data/users.json"
ROLES_FILE = "data/access_roles.json"

# --------------------- Utility Functions ---------------------

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

# --------------------- Role Checking ---------------------

def get_role_by_passcode(passcode):
    roles = load_json(ROLES_FILE)
    return roles.get(passcode.strip())

# --------------------- User Functions ---------------------

def register_user(email, password, passcode=None):
    users = load_json(USER_FILE)

    if any(u["email"].lower() == email.lower() for u in users):
        return {"error": "User already exists."}

    role = get_role_by_passcode(passcode) if passcode else "user"
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": hash_password(password),
        "role": role,
        "membership": "guest" if role == "user" else "basic",  # defaults
        "language": "en",
        "theme": "dark",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    users.append(user)
    save_json(USER_FILE, users)
    return {"success": True, "user": user}

def authenticate_user(email, password):
    users = load_json(USER_FILE)
    for user in users:
        if user["email"].lower() == email.lower() and verify_password(password, user["password"]):
            return user
    return None

def get_user_by_email(email):
    users = load_json(USER_FILE)
    for user in users:
        if user["email"].lower() == email.lower():
            return user
    return None

def update_user(email, field, value):
    users = load_json(USER_FILE)
    updated = False
    for user in users:
        if user["email"].lower() == email.lower():
            user[field] = value
            updated = True
            break
    if updated:
        save_json(USER_FILE, users)
    return updated

def set_membership(email, new_plan):
    return update_user(email, "membership", new_plan)

def set_theme(email, theme_name):
    return update_user(email, "theme", theme_name)

def set_language(email, lang_code):
    return update_user(email, "language", lang_code)

