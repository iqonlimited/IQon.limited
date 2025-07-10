# modules/ai_training.py

import json
import os

TRAINING_FILE = "data/qa_data.json"
TRAINING_LOG = "data/ai_training_logs.json"

def load_training_data():
    if not os.path.exists(TRAINING_FILE):
        return {}
    with open(TRAINING_FILE, "r") as f:
        return json.load(f)

def save_training_data(data):
    with open(TRAINING_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_training_logs():
    if not os.path.exists(TRAINING_LOG):
        return []
    with open(TRAINING_LOG, "r") as f:
        return json.load(f)

def save_training_logs(logs):
    with open(TRAINING_LOG, "w") as f:
        json.dump(logs, f, indent=4)

def add_question_answer(question, answers_by_plan, added_by):
    data = load_training_data()
    logs = load_training_logs()

    data[question.lower()] = answers_by_plan

    logs.append({
        "question": question,
        "answers": answers_by_plan,
        "added_by": added_by,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    })

    save_training_data(data)
    save_training_logs(logs)

def get_answer_by_plan(question, membership_level):
    data = load_training_data()
    q_data = data.get(question.lower(), {})
    return q_data.get(membership_level) or q_data.get("default")
