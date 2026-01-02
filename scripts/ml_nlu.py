import json
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Machine Learning – Natural Language Understanding
def load_training_data(data_folder=None):
    if data_folder is None:
        base_dir = os.path.dirname(__file__)
        data_folder = os.path.abspath(os.path.join(base_dir, "..", "data", "intents"))

    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"❌ Intent folder not found: {data_folder}")

    training_data = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            with open(os.path.join(data_folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)

                if "intent" not in data or "utterances" not in data:
                    raise KeyError(f"❌ Invalid JSON format in {filename}")

                intent = data["intent"]
                for utterance in data["utterances"]:
                    if utterance.strip():
                        training_data.append((utterance, intent))

    if not training_data:
        raise ValueError("❌ No training samples loaded. Check your JSON utterances.")

    print(f"✅ Loaded {len(training_data)} training samples", file=sys.stderr)
    return training_data

class IntentClassifier:
    def __init__(self, training_data):
        texts, labels = zip(*training_data)

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                token_pattern=r"(?u)\b\w+\b"
            )),
            ("clf", LinearSVC())
        ])

        self.pipeline.fit(texts, labels)

    def predict_with_confidence(self, text):
        scores = self.pipeline.decision_function([text])
        max_score = max(scores[0])
        intent = self.pipeline.predict([text])[0]
        return intent, max_score
        self.pipeline.fit(texts, labels)

    def predict(self, text):
        return self.pipeline.predict([text])[0]