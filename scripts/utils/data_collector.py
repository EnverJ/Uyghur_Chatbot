import json
import os

BASE_DIR = os.path.dirname(__file__)

def save_fallback_input(user_text):
    """
    Save unknown user inputs into data/intents/userInput.json
    using the same structure as other intent files.
    """

    file_path = os.path.join(
        BASE_DIR, "..","..", "data", "intents", "newInputs","userInput.json"
    )

    # Load existing file or initialize new structure
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "intent": "unlabeled",
            "utterances": []
        }

    # Avoid duplicates
    if user_text not in data["utterances"]:
        data["utterances"].append(user_text)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)