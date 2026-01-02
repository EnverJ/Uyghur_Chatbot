# Uyghur Chatbot Project

This project is a simple Uyghur language chatbot using a machine learning-based intent classifier and JSON-based responses.  

---

## **Project Structure**

Uyghur_Chatbot/
├── app.py                   # Main entry point to run the chatbot
├── ml_nlu.py                # ML intent classifier and training data loader
├── response_loader.py       # Loads and validates responses
├── data/
│   ├── intents/             # Training utterances for each intent
│   │   ├── greeting.json
│   │   ├── thanks.json
│   │   └── farewell.json
│   └── responses/           # Responses for each intent
│       ├── greeting.json
│       ├── thanks.json
│       ├── farewell.json
│       └── fallback.json    # Mandatory fallback responses
├── requirements.txt         # Python dependencies (optional)

---

## **File Descriptions**

### 1. `app.py` ✅ Required
- **Purpose:** Main entry point to run the chatbot.
- **Functionality:**  
  - Loads the training data from `data/intents/`  
  - Trains the ML-based intent classifier (`ml_nlu.py`)  
  - Loads response JSONs (`response_loader.py`)  
  - Starts the interactive chat loop

---

### 2. `ml_nlu.py` ✅ Required
- **Purpose:** Handles Natural Language Understanding (NLU).
- **Functionality:**  
  - `IntentClassifier` trains a model on intent utterances  
  - `load_training_data()` reads `data/intents/` JSON files  
  - Predicts the intent of user input

---

### 3. `response_loader.py` ✅ Required
- **Purpose:** Loads and validates chatbot responses.
- **Functionality:**  
  - Reads JSON files from `data/responses/`  
  - Ensures each file has `"intent"` and `"responses"` keys  
  - Confirms a `"fallback"` intent exists  
  - Returns a dictionary mapping intents to responses

---

### 4. `data/intents/` ✅ Required
- **Purpose:** Stores JSON files containing user utterances for each intent.
- **Example JSON Structure:**
```json
{
  "intent": "greeting",
  "utterances": [
    "سالام",
    "ياخشىمۇسىز"
  ]
}

---
```### 5. `data/responses/` ✅ Required
- **Purpose:** Stores JSON files containing chatbot responses for each intent.
ml_nlu.py is the machine learning component of our chatbot. 
It loads labeled training examples for each intent,
turns the text into numerical features (using TF‑IDF),
and trains a classifier (SVM) to recognize user intent.
When a user sends a message, 
it predicts the corresponding intent and a confidence score, 
which the chatbot uses to select an appropriate response.
