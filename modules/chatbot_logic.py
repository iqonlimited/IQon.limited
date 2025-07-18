import json
import requests

def get_answer_from_json(user_input, role, json_file="data/qa_data.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Check for role-specific answers
        role_data = data.get(role, [])
        for qa in role_data:
            if qa['question'].lower() == user_input.lower():
                return qa['answer']
        # Check for guest answers if not found in role
        for qa in data.get('guest', []):
            if qa['question'].lower() == user_input.lower():
                return qa['answer']
        return None
    except Exception as e:
        print(f"[Error] {e}")
        return None

def get_fallback_ai_response(user_input):
    try:
        payload = {"model": "mistral", "prompt": user_input}
        r = requests.post("http://localhost:11434/api/generate", json=payload)
        if r.status_code == 200:
            return r.json().get("response", "I don't know.")
        else:
            return "AI service not responding."
    except Exception as e:
        print(f"[Fallback Error] {e}")
        return "Sorry, I have no idea about that."
