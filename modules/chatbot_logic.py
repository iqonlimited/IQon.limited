import json
import requests

def get_answer_from_json(user_input, role, json_file="data/qa_data.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for qa in data.get(role, []):
            if qa['question'].lower() == user_input.lower():
                return qa['answer']
        return None
    except:
        return None

def get_fallback_ai_response(user_input):
    try:
        payload = {"model": "mistral", "prompt": user_input}
        r = requests.post("http://localhost:11434/api/generate", json=payload)
        return r.json().get("response", "I don't know.")
    except:
        return "Sorry, I have no answer."
