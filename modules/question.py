import json
import os
import uuid
from datetime import datetime

QUESTIONS_FILE = "data/qa_data.json"

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(questions):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

def add_question(question_text, answers_by_plan, added_by="admin", tags=None):
    questions = load_questions()
    new_entry = {
        "id": str(uuid.uuid4()),
        "question": question_text.strip(),
        "answers": answers_by_plan,  # Dict: {"basic": "A1", "intermediate": "A2", ...}
        "added_by": added_by,
        "tags": tags or [],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    questions.append(new_entry)
    save_questions(questions)
    return new_entry

def get_answer_for_user(question_text, user_membership):
    questions = load_questions()
    for q in questions:
        if q["question"].strip().lower() == question_text.strip().lower():
            return q["answers"].get(user_membership.lower()) or q["answers"].get("basic")
    return None  # Not found

def get_all_questions():
    return load_questions()

def get_questions_by_tag(tag):
    return [q for q in load_questions() if tag in q.get("tags", [])]

def delete_question(question_id):
    questions = load_questions()
    updated = [q for q in questions if q["id"] != question_id]
    if len(updated) == len(questions):
        return False
    save_questions(updated)
    return True

def update_question(question_id, new_data):
    questions = load_questions()
    updated = False
    for q in questions:
        if q["id"] == question_id:
            q.update(new_data)
            updated = True
            break
    if updated:
        save_questions(questions)
    return updated
