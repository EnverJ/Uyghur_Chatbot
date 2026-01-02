from utils.categorizer import load_user_inputs, label_utterance, create_intent_file
from ml_nlu import IntentClassifier, load_training_data
import os

# Load classifier
training_data = load_training_data()
classifier = IntentClassifier(training_data)

# Confidence threshold for auto-labeling
AUTO_CONFIDENCE_THRESHOLD = 0.8

def list_intents():
    from utils.categorizer import INTENT_DIR
    return [f.split(".json")[0] for f in os.listdir(INTENT_DIR) if f.endswith(".json")]

def suggest_intent(text):
    """Use classifier to predict intent and confidence"""
    intent, confidence = classifier.predict_with_confidence(text)
    return str(intent), confidence

def main():
    while True:
        inputs = load_user_inputs()
        if not inputs:
            print("✅ No unlabeled user inputs.")
            break

        # Show all unlabeled inputs
        print("\nUnlabeled inputs:")
        for i, text in enumerate(inputs, start=1):
            print(f"{i}. {text}")

        # Let admin select one input
        choice = input("\nSelect input to label (number) or 'q' to quit: ").strip()
        if choice.lower() == 'q':
            print("⚡ Admin stopped the labeling process.")
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(inputs):
            print("❌ Invalid selection. Try again.")
            continue

        idx = int(choice) - 1
        text_to_label = inputs[idx]

        # Get classifier suggestion
        suggested_intent, confidence = suggest_intent(text_to_label)
        print(f"\n💡 Suggested intent: '{suggested_intent}' (confidence: {confidence:.2f})")

        intents = list_intents()
        print("\nAvailable intents:")
        for i, intent in enumerate(intents, start=1):
            print(f"{i}. {intent}")
        print(f"{len(intents)+1}. [Create new intent]")
        print(f"{len(intents)+2}. [Use suggested intent]")
        print(f"{len(intents)+3}. [Skip this input]")
        print(f"{len(intents)+4}. [Quit without labeling]")

        while True:
            intent_choice = input("Select target intent (number): ").strip()
            if not intent_choice.isdigit():
                print("❌ Invalid input. Enter a number.")
                continue

            intent_choice = int(intent_choice)

            if intent_choice == len(intents)+1:
                # Create new intent
                new_intent_name = input("Enter new intent name: ").strip()
                if not new_intent_name:
                    print("❌ Intent name cannot be empty.")
                    continue
                create_intent_file(new_intent_name)
                target_intent = new_intent_name
                break
            elif intent_choice == len(intents)+2:
                # Use suggested intent
                target_intent = suggested_intent
                break
            elif intent_choice == len(intents)+3:
                # Skip input
                print(f"⚡ Skipped input: {text_to_label}")
                target_intent = None
                break
            elif intent_choice == len(intents)+4:
                # Quit labeling without touching this input
                print(f"⚡ Quit without labeling input: {text_to_label}")
                return
            elif 1 <= intent_choice <= len(intents):
                target_intent = intents[intent_choice-1]
                break
            else:
                print("❌ Invalid selection. Try again.")

        if target_intent:
            label_utterance(text_to_label, target_intent)

if __name__ == "__main__":
    main()