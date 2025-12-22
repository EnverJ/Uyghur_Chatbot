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

CONFIDENCE_THRESHOLD = 0.00  # you can tune this
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()

    intent, confidence = classifier.predict_with_confidence(message)
    intent = str(intent)

    # 🔴 HARD STOP FOR UNKNOWN INPUT
    if confidence < CONFIDENCE_THRESHOLD:
        save_fallback_input(message)

        return jsonify({
            "reply": random.choice(RESPONSES["fallback"]),
            "intent": "fallback",
            "confidence": round(confidence, 2)})
    # ✅ ONLY known, confident inputs reach here
    return jsonify({
        "reply": random.choice(RESPONSES.get(intent, RESPONSES["fallback"])),
        "intent": intent,
        "confidence": round(confidence, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)