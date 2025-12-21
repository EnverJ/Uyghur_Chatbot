from nlu import detect_intent
from response import RESPONSES
import random

print("🤖 Uyghur Chatbot (type 'exit' to quit)n/🤖 ئۇيغۇرچە روبوتقا خوش كەپسىز!")
while True:
    user_input = input("👤: ")
    if user_input.lower() == "exit":
        print("🤖 Goodbye!!خەير-خوش")
        break

    intent = detect_intent(user_input)
    responses = RESPONSES.get(intent, RESPONSES["fallback"])
    # bot_response = responses[0]  # Always pick the first response for simplicity
    # print(f"🤖 Bot: {bot_response}")
    # pick up first response
    # print(f"🤖: {responses[0]}")
    # pick up random response
    ransomResponses = RESPONSES.get(intent, RESPONSES["fallback"])
    reply = random.choice(ransomResponses)

    print(f"🤖: {reply}")

