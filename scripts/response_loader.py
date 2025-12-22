import json
import os

def load_responses(response_folder="../data/responses"):
    responses = {}

    for filename in os.listdir(response_folder):
        if filename.endswith(".json"):
            with open(os.path.join(response_folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                intent = data["intent"]
                responses[intent] = data["responses"]

    return responses