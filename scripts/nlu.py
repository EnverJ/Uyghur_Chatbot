# Natural Language Understanding.
from intent import INTENTS
def detect_intent(user_input):
    user_input = user_input.strip()
    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            if phrase in user_input:
                return intent
    return "unknown"