import json
import uuid
import datetime
from modules.helper import load_json, save_json

FORUM_FILE = "data/forum.json"

# --------------------------
# UTILITY FUNCTIONS
# --------------------------

def get_forum_data():
    return load_json(FORUM_FILE)

def save_forum_data(data):
    save_json(FORUM_FILE, data)

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.datetime.utcnow().isoformat()

# --------------------------
# QUESTION MANAGEMENT
# --------------------------

def post_question(user_id, username, title, content, tags=[]):
    data = get_forum_data()
    question_id = generate_id()
    
    question = {
        "id": question_id,
        "user_id": user_id,
        "username": username,
        "title": title,
        "content": content,
        "tags": tags,
        "timestamp": get_timestamp(),
        "answers": [],
        "votes": 0,
        "status": "active"  # could be "active", "closed", "deleted"
    }

    data["questions"][question_id] = question
    save_forum_data(data)
    return question_id

def get_all_questions():
    data = get_forum_data()
    return list(data["questions"].values())

def get_question_by_id(qid):
    data = get_forum_data()
    return data["questions"].get(qid)

def delete_question(qid, admin=False):
    data = get_forum_data()
    if qid in data["questions"]:
        if admin:
            del data["questions"][qid]
        else:
            data["questions"][qid]["status"] = "deleted"
        save_forum_data(data)
        return True
    return False

# --------------------------
# ANSWERS
# --------------------------

def add_answer(qid, user_id, username, content):
    data = get_forum_data()
    answer_id = generate_id()

    answer = {
        "id": answer_id,
        "user_id": user_id,
        "username": username,
        "content": content,
        "timestamp": get_timestamp(),
        "votes": 0
    }

    if qid in data["questions"]:
        data["questions"][qid]["answers"].append(answer)
        save_forum_data(data)
        return answer_id
    return None

# --------------------------
# VOTING
# --------------------------

def vote_question(qid, upvote=True):
    data = get_forum_data()
    if qid in data["questions"]:
        if upvote:
            data["questions"][qid]["votes"] += 1
        else:
            data["questions"][qid]["votes"] -= 1
        save_forum_data(data)
        return True
    return False

def vote_answer(qid, answer_id, upvote=True):
    data = get_forum_data()
    if qid in data["questions"]:
        for answer in data["questions"][qid]["answers"]:
            if answer["id"] == answer_id:
                if upvote:
                    answer["votes"] += 1
                else:
                    answer["votes"] -= 1
                save_forum_data(data)
                return True
    return False
