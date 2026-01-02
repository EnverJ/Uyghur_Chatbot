from flask import Flask, request, jsonify, render_template
from ml_nlu import IntentClassifier, load_training_data
from response_loader import load_responses
from utils.data_collector import save_fallback_input
import random, os

app = Flask(__name__)

# Load training data and responses
training_data = load_training_data("../data/intents")
classifier = IntentClassifier(training_data)
RESPONSES = load_responses("../data/responses")

# Home page route
@app.route("/")
def index():
    return render_template("index.html")

# Confidence threshold for fallback
CONFIDENCE_THRESHOLD = 0.0  # tune as needed

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "⚠️ Please type something.",
            "intent": None,
            "confidence": 0
        })

    intent, confidence = classifier.predict_with_confidence(message)
    intent = str(intent)

    # 🔴 Unknown or low-confidence input → fallback
    if confidence < CONFIDENCE_THRESHOLD or intent not in RESPONSES:
        # Save input to both userInput.json and backup with timestamp
        save_fallback_input(message)

        return jsonify({
            "reply": random.choice(RESPONSES.get("fallback", ["I’m sorry, I didn’t understand that."])),
            "intent": "fallback",
            "confidence": round(confidence, 2)
        })

    # ✅ Known, confident input
    return jsonify({
        "reply": random.choice(RESPONSES.get(intent, RESPONSES.get("fallback", ["I’m sorry, I didn’t understand that."]))),
        "intent": intent,
        "confidence": round(confidence, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)