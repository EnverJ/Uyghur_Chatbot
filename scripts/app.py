import random
from ml_nlu import IntentClassifier, load_training_data
from response_loader import load_responses
import os


def main():
    # Load training data and train classifier
    training_data = load_training_data()
    classifier = IntentClassifier(training_data)

    # Load responses

    base_dir = os.path.dirname(__file__)  # folder where app.py lives
    responses_folder = os.path.join(base_dir, "..", "data", "responses")
    RESPONSES = load_responses(responses_folder)

    print("🤖 Uyghur Chatbot (type 'exit' to quit)")

    while True:
        user_input = input("👤: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("🤖: خوش!")
            break

        intent = classifier.predict(user_input)
        response_list = RESPONSES.get(intent, RESPONSES["fallback"])
        reply = random.choice(response_list)

        print(f"🤖: {reply}")


if __name__ == "__main__":
    main()