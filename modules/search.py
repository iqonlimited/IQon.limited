import os
import json
from modules.helper import load_json

# File paths
CHAT_HISTORY_FILE = "data/chat_history.json"
EBOOKS_FILE = "data/ebooks.json"
NOTIFICATION_FILE = "data/notifications.json"
UPLOADS_DIR = "static/uploads/"

# --------------- SEARCH UTILITIES -----------------

def search_chats(query, user_id):
    """Search user-specific chat history for a query."""
    history = load_json(CHAT_HISTORY_FILE)
    results = []

    if user_id in history:
        for item in history[user_id]:
            if query.lower() in item["question"].lower() or query.lower() in item["answer"].lower():
                results.append(item)

    return results

def search_ebooks(query):
    """Search all uploaded ebooks by title, author, or tags."""
    ebooks = load_json(EBOOKS_FILE)
    results = []

    for ebook in ebooks.values():
        if (query.lower() in ebook.get("title", "").lower() or
            query.lower() in ebook.get("author", "").lower() or
            query.lower() in ebook.get("tags", "").lower()):
            results.append(ebook)

    return results

def search_notifications(query, user_role="user"):
    """Search notifications relevant to a user role."""
    notifications = load_json(NOTIFICATION_FILE)
    results = []

    for note in notifications.values():
        if (note["audience"] in [user_role, "all"] and query.lower() in note["message"].lower()):
            results.append(note)

    return results

def search_uploaded_files(query):
    """Search filenames across upload directories."""
    matched_files = []
    for folder in ["ebooks", "audio", "images", "videos", "temp"]:
        path = os.path.join(UPLOADS_DIR, folder)
        if os.path.exists(path):
            for file in os.listdir(path):
                if query.lower() in file.lower():
                    matched_files.append({
                        "file": file,
                        "folder": folder,
                        "path": f"{UPLOADS_DIR}{folder}/{file}"
                    })
    return matched_files

# ---------------- GLOBAL SEARCH --------------------

def global_search(query, user_id=None, user_role="user"):
    """
    Returns a dictionary of search results across all systems:
    - Chat History
    - Ebooks
    - Notifications
    - Uploaded Files
    """
    return {
        "chats": search_chats(query, user_id) if user_id else [],
        "ebooks": search_ebooks(query),
        "notifications": search_notifications(query, user_role),
        "files": search_uploaded_files(query)
    }
