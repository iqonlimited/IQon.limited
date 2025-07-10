# modules/analytics.py

import json
import os
from datetime import datetime

DATA_FILE = "data/analytics.json"

def load_analytics():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_analytics(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_chat(user_email, location="Unknown"):
    data = load_analytics()
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in data:
        data[today] = {}

    if user_email not in data[today]:
        data[today][user_email] = {"chats": 0, "location": location}
    
    data[today][user_email]["chats"] += 1
    save_analytics(data)

def get_leaderboard():
    data = load_analytics()
    leaderboard = {}

    for day in data:
        for user_email, stats in data[day].items():
            leaderboard[user_email] = leaderboard.get(user_email, 0) + stats["chats"]

    sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return sorted_lb

def get_daily_chat_count():
    data = load_analytics()
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(stats["chats"] for stats in data.get(today, {}).values())
