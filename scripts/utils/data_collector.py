import json
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..", "data", "intents"))
NEW_INPUTS_DIR = os.path.join(BASE_DIR, "newInputs")

USER_INPUT_FILE = os.path.join(NEW_INPUTS_DIR, "userInput.json")
USER_INPUT_BACKUP_FILE = os.path.join(NEW_INPUTS_DIR, "userInput_backup.json")

def _load_backup_texts():
    if os.path.exists(USER_INPUT_BACKUP_FILE):
        with open(USER_INPUT_BACKUP_FILE, "r", encoding="utf-8") as f:
            backup_data = json.load(f)
        return [entry["text"] for entry in backup_data.get("entries", [])]
    return []

def _load_current_inputs():
    if os.path.exists(USER_INPUT_FILE):
        with open(USER_INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("utterances", [])
    return []
def _load_all_categorized():
    texts = []
    for fname in os.listdir(BASE_DIR):
        if fname.endswith(".json"):
            path = os.path.join(BASE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                texts.extend(data.get("utterances", []))
    return texts

def save_fallback_input(user_text):
    """
    Save unknown user input *only* if it has never been seen before:
    in current queue, historical backup, or already categorized.
    """
    os.makedirs(NEW_INPUTS_DIR, exist_ok=True)

    text = user_text.strip()

    # Load all sets
    current_inputs = _load_current_inputs()
    backup_texts = _load_backup_texts()
    categorized_texts = _load_all_categorized()

    # Skip if already in any set
    if text in current_inputs or text in backup_texts or text in categorized_texts:
        return

    # Otherwise save as new
    # 1) Add to current
    current_inputs.append(text)
    with open(USER_INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"intent": "unlabeled", "utterances": current_inputs},
                  f, ensure_ascii=False, indent=2)

    # 2) Add to backup with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    backup_entries = []
    if os.path.exists(USER_INPUT_BACKUP_FILE):
        with open(USER_INPUT_BACKUP_FILE, "r", encoding="utf-8") as f:
            backup_data = json.load(f)
            backup_entries = backup_data.get("entries", [])

    backup_entries.append({"text": text, "timestamp": timestamp})
    with open(USER_INPUT_BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump({"entries": backup_entries}, f, ensure_ascii=False, indent=2)

RESPONSES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..", "data", "responses"))
def create_response_file(intent_name):
    '''
    create a basic response file for a new intent if it does not exist
    and ask the admin to optionally add initial responses
    '''
    os.makedirs(RESPONSES_DIR, exist_ok=True)
    file_path = os.path.join(RESPONSES_DIR, f"{intent_name}.json")
#     if the file already exists, do nothing
    if os.path.exists(file_path):
        return file_path;
    # ask admin if they want to add initial responses now
    print(f"\nNew intent '{intent_name}' created!")
    resp_now= input("Would you like to add initial responses now? (y/n): ").strip().lower()
    # default placeholder responses
    responses = [
        "I'm sorry, I don't have a response for that yet.",
        "Could you please rephrase your question?"
    ]
    if resp_now == 'y':
        print("Enter responses one by one. Type 'done' when finished:")
        responses = []
        while True:
            resp = input("Response: ").strip()
            if resp.lower() == 'done':
                break
            if resp:
                responses.append(resp)
        if not responses:
            responses = [
                "I'm sorry, I don't have a response for that yet.",
                "Could you please rephrase your question?"
            ]
    # save the responses to the file
    data = {"intent": intent_name, "responses": responses}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"⚡ Created new response file: {intent_name}\n")
    return file_path

