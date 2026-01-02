from flask import Flask, request, jsonify, render_template
import random, os

from ml_nlu import IntentClassifier, load_training_data
from response_loader import load_responses
from utils.data_collector_ui import save_fallback_input, load_user_inputs, label_utterance, create_intent_file

app = Flask(__name__)

# Load classifier and responses
training_data = load_training_data("../data/intents")
classifier = IntentClassifier(training_data)
RESPONSES = load_responses("../data/responses"]
CONFIDENCE_THRESHOLD = 0.6  # tweak if needed

# ------------------ CHAT ROUTE ------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "⚠️ Please type something.", "intent": None, "confidence": 0})

    intent, confidence = classifier.predict_with_confidence(message)
    intent = str(intent)

    if confidence < CONFIDENCE_THRESHOLD or intent not in RESPONSES:
        save_fallback_input(message)
        return jsonify({
            "reply": random.choice(RESPONSES.get("fallback", ["I’m sorry, I didn’t understand that."])),
            "intent": "fallback",
            "confidence": round(confidence, 2)
        })

    return jsonify({
        "reply": random.choice(RESPONSES.get(intent, RESPONSES["fallback"])),
        "intent": intent,
        "confidence": round(confidence, 2)
    })

# ------------------ ADMIN UI ------------------

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_label.html")


@app.get("/admin/unlabeled")
def get_unlabeled_inputs():
    inputs = load_user_inputs()
    return jsonify({"unlabeled": inputs})


@app.post("/admin/label")
def admin_label():
    data = request.json
    text = data.get("text")
    intent = data.get("intent")

    if not text or not intent:
        return jsonify({"status": "error", "message": "Missing text or intent"}), 400

    label_utterance(text, intent)
    return jsonify({"status": "ok"})


@app.post("/admin/create_intent")
def admin_create_intent():
    data = request.json
    intent_name = data.get("intent")

    if not intent_name:
        return jsonify({"status": "error", "message": "Intent name is required"}), 400

    create_intent_file(intent_name)
    return jsonify({"status": "ok"})

# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)