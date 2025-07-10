import json
import os
from datetime import datetime
from modules.helper import load_json, save_json, generate_id, get_current_time

# Path to notifications file
NOTIFICATION_FILE = "data/notifications.json"
USER_FILE = "data/users.json"

# ---------------------- Notification Core ----------------------

def create_notification(message, sender, audience="all", level="info"):
    """
    Create a new notification. Audience can be 'all', 'user', 'employee', or 'admin'.
    """
    notifications = load_json(NOTIFICATION_FILE)
    notification_id = generate_id()
    
    notification = {
        "id": notification_id,
        "timestamp": get_current_time(),
        "message": message,
        "sender": sender,
        "audience": audience,
        "level": level,
        "read_by": []
    }

    notifications[notification_id] = notification
    save_json(NOTIFICATION_FILE, notifications)
    return notification

def get_user_notifications(user_id, role="user"):
    """
    Return all unread or relevant notifications for a specific user.
    """
    notifications = load_json(NOTIFICATION_FILE)
    relevant = []

    for n in notifications.values():
        if (n["audience"] == "all" or n["audience"] == role) and user_id not in n["read_by"]:
            relevant.append(n)
    
    return sorted(relevant, key=lambda x: x["timestamp"], reverse=True)

def mark_as_read(notification_id, user_id):
    """
    Mark a notification as read by a specific user.
    """
    notifications = load_json(NOTIFICATION_FILE)
    if notification_id in notifications:
        if user_id not in notifications[notification_id]["read_by"]:
            notifications[notification_id]["read_by"].append(user_id)
        save_json(NOTIFICATION_FILE, notifications)

def delete_notification(notification_id):
    """
    Admin/employee can delete a notification by ID.
    """
    notifications = load_json(NOTIFICATION_FILE)
    if notification_id in notifications:
        del notifications[notification_id]
        save_json(NOTIFICATION_FILE, notifications)

# ---------------------- Bulk Send ----------------------

def send_to_all_users(message, sender="admin"):
    """
    Sends a notification to every registered user.
    """
    users = load_json(USER_FILE)
    for role in ["user", "employee", "admin"]:
        create_notification(message, sender, audience=role)
