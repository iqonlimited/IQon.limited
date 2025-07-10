import json
import os
import uuid
from datetime import datetime

FEEDBACK_FILE = "data/feedback.json"

def load_feedback():
    """Load all feedback entries from JSON."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_feedback(feedback_list):
    """Save all feedback entries to JSON."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_list, f, indent=4, ensure_ascii=False)

def add_feedback(user_email, feedback_text, rating, feature="General"):
    """Add new feedback."""
    feedback_list = load_feedback()
    new_feedback = {
        "id": str(uuid.uuid4()),
        "user_email": user_email,
        "text": feedback_text,
        "rating": float(rating),
        "feature": feature,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    feedback_list.append(new_feedback)
    save_feedback(feedback_list)
    return new_feedback

def get_all_feedback():
    """Get all feedback entries."""
    return load_feedback()

def get_feedback_by_feature(feature_name):
    """Get feedback related to a specific feature."""
    return [fb for fb in load_feedback() if fb["feature"].lower() == feature_name.lower()]

def get_feedback_by_user(user_email):
    """Get feedback submitted by a specific user."""
    return [fb for fb in load_feedback() if fb["user_email"].lower() == user_email.lower()]

def delete_feedback(feedback_id):
    """Delete a feedback entry by ID."""
    feedback_list = load_feedback()
    new_list = [fb for fb in feedback_list if fb["id"] != feedback_id]
    if len(new_list) == len(feedback_list):
        return False
    save_feedback(new_list)
    return True
