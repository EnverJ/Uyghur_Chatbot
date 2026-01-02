from utils.data_collector import load_user_inputs
from ml_nlu import IntentClassifier, load_training_data

# Load classifier once for suggestions
training_data = load_training_data()
classifier = IntentClassifier(training_data)

def get_unlabeled_with_suggestions():
    """
    Return a list of dicts:
    [
        { "text": "...", "suggested_intent": "...", "confidence": 0.XX },
        ...
    ]
    """
    inputs = load_user_inputs()
    results = []

    for text in inputs:
        intent, confidence = classifier.predict_with_confidence(text)
        results.append({
            "text": text,
            "suggested_intent": intent,
            "confidence": round(confidence, 2)
        })

    return results