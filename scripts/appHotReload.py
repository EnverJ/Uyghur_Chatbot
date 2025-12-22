import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ml_nlu import IntentClassifier, load_training_data
from response_loader import load_responses
import os, random

DATA_INTENTS = "../data/intents"
DATA_RESPONSES = "../data/responses"

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_callback):
        self.reload_callback = reload_callback

    def on_modified(self, event):
        if event.src_path.endswith(".json"):
            print("🔄 Detected change in JSON, reloading...")
            self.reload_callback()

def main():
    classifier = None
    RESPONSES = None

    # Function to reload training data and responses
    def reload_all():
        nonlocal classifier, RESPONSES
        training_data = load_training_data(DATA_INTENTS)
        classifier = IntentClassifier(training_data)
        RESPONSES = load_responses(DATA_RESPONSES)
        print(f"✅ Reloaded: {len(training_data)} training samples, {len(RESPONSES)} intents")

    # Initial load
    reload_all()

    # Set up watcher
    event_handler = ReloadHandler(reload_all)
    observer = Observer()
    observer.schedule(event_handler, path=DATA_INTENTS, recursive=True)
    observer.schedule(event_handler, path=DATA_RESPONSES, recursive=True)
    observer.start()

    print("🤖 Uyghur Chatbot (type 'exit' to quit)")

    try:
        while True:
            user_input = input("👤: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("🤖: خوش!")
                break

            intent = classifier.predict(user_input)
            response_list = RESPONSES.get(intent, RESPONSES["fallback"])
            reply = random.choice(response_list)
            print(f"🤖: {reply}")
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()