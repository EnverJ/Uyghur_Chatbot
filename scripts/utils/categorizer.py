import json
import os

from scripts.utils.data_collector import create_response_file

# Base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTENT_DIR = os.path.join(BASE_DIR, "data", "intents")
USER_INPUT_FILE = os.path.join(INTENT_DIR, "newInputs", "userInput.json")


def load_user_inputs():
    """Load user inputs saved for future labeling."""
    if not os.path.exists(USER_INPUT_FILE):
        return []

    with open(USER_INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("utterances", [])


def create_intent_file(intent_name):
    """Create a new intent JSON file if it does not exist."""
    intent_file = os.path.join(INTENT_DIR, f"{intent_name}.json")
    if not os.path.exists(intent_file):
        data = {"intent": intent_name, "utterances": []}
        with open(intent_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"⚡ Created new intent file: {intent_name}.json")
    # Also create the corresponding response file if missing
    create_response_file(intent_name)
    return intent_file


def label_utterance(text, target_intent):
    """
    Label a user input and move it to the correct intent file.
    Auto-creates the intent file if it does not exist.
    """

    # Ensure intent file exists
    intent_file = create_intent_file(target_intent)

    # Load intent file
    with open(intent_file, "r", encoding="utf-8") as f:
        intent_data = json.load(f)

    # Add utterance if not already present
    if text not in intent_data["utterances"]:
        intent_data["utterances"].append(text)

    # Save intent file
    with open(intent_file, "w", encoding="utf-8") as f:
        json.dump(intent_data, f, ensure_ascii=False, indent=2)

    # Remove from userInput.json
    if os.path.exists(USER_INPUT_FILE):
        with open(USER_INPUT_FILE, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        if text in user_data.get("utterances", []):
            user_data["utterances"].remove(text)

        with open(USER_INPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Labeled & moved: '{text}' → {target_intent}.json")