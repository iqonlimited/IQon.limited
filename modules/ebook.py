import json
import os
import uuid
from datetime import datetime

EBOOKS_FILE = "data/ebooks.json"

def load_ebooks():
    """Load all ebooks from JSON."""
    if not os.path.exists(EBOOKS_FILE):
        return []
    with open(EBOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ebooks(ebooks):
    """Save all ebooks to JSON."""
    with open(EBOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(ebooks, f, indent=4, ensure_ascii=False)

def add_ebook(title, author, filename, cover_image, price, uploader, category="General", language="English", description=""):
    """Add a new ebook to the library."""
    ebooks = load_ebooks()
    new_ebook = {
        "id": str(uuid.uuid4()),
        "title": title,
        "author": author,
        "filename": filename,
        "cover_image": cover_image,
        "price": float(price),
        "uploader": uploader,
        "category": category,
        "language": language,
        "description": description,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 0,
        "downloads": 0,
        "purchases": []
    }
    ebooks.append(new_ebook)
    save_ebooks(ebooks)
    return new_ebook

def get_all_ebooks():
    """Return all ebooks."""
    return load_ebooks()

def get_ebook_by_id(ebook_id):
    """Find ebook by its unique ID."""
    for ebook in load_ebooks():
        if ebook["id"] == ebook_id:
            return ebook
    return None

def get_ebooks_by_uploader(email):
    """Return all ebooks uploaded by a specific user."""
    return [ebook for ebook in load_ebooks() if ebook["uploader"] == email]

def update_ebook(ebook_id, **kwargs):
    """Update fields of an ebook by ID."""
    ebooks = load_ebooks()
    updated = False
    for ebook in ebooks:
        if ebook["id"] == ebook_id:
            for key, value in kwargs.items():
                if key in ebook:
                    ebook[key] = value
            updated = True
            break
    if updated:
        save_ebooks(ebooks)
    return updated

def delete_ebook(ebook_id):
    """Delete an ebook by ID."""
    ebooks = load_ebooks()
    updated_list = [ebook for ebook in ebooks if ebook["id"] != ebook_id]
    if len(ebooks) == len(updated_list):
        return False
    save_ebooks(updated_list)
    return True

def increment_view(ebook_id):
    """Increment the view count for an ebook."""
    ebooks = load_ebooks()
    for ebook in ebooks:
        if ebook["id"] == ebook_id:
            ebook["views"] += 1
            save_ebooks(ebooks)
            return True
    return False

def increment_download(ebook_id):
    """Increment the download count for an ebook."""
    ebooks = load_ebooks()
    for ebook in ebooks:
        if ebook["id"] == ebook_id:
            ebook["downloads"] += 1
            save_ebooks(ebooks)
            return True
    return False

def record_purchase(ebook_id, user_email):
    """Track who purchased the ebook."""
    ebooks = load_ebooks()
    for ebook in ebooks:
        if ebook["id"] == ebook_id:
            if user_email not in ebook["purchases"]:
                ebook["purchases"].append(user_email)
                save_ebooks(ebooks)
            return True
    return False

def has_user_purchased(ebook_id, user_email):
    """Check if a user has purchased an ebook."""
    ebook = get_ebook_by_id(ebook_id)
    if ebook and user_email in ebook.get("purchases", []):
        return True
    return False
