import ollama
import pandas as pd
import csv
from pathlib import Path
from datetime import datetime

# Project paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"

HISTORY_FILE = DATASET_DIR / "chat_history.csv"
RESPONSES_FILE = DATASET_DIR / "responses.csv"
LOG_FILE = DATASET_DIR / "chatbot_logs.txt"

MODEL_NAME = "llama3.2:latest"

# Create dataset folder if needed
DATASET_DIR.mkdir(exist_ok=True)

# Conversation history for context
conversation_history = []

# Create CSV files with headers if they do not exist
for file_path in [HISTORY_FILE, RESPONSES_FILE]:
    if not file_path.exists():
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "TIMESTAMP",
                "SESSION_ID",
                "ROLE",
                "MESSAGE"
            ])

print("=" * 50)
print("EDUCATION CHATBOT - WEEK 9")
print("Model:", MODEL_NAME)
print("Type 'exit' to stop the chatbot.")
print("=" * 50)

session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! Keep learning!")
        break

    if not user_input:
        print("Chatbot: Please enter a question.")
        continue

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add user message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly education assistant. "
                        "Explain concepts in simple English. "
                        "Give accurate, clear, student-friendly answers. "
                        "For coding questions, provide simple examples."
                    )
                },
                *conversation_history
            ]
        )

        answer = response["message"]["content"]
        print("\nChatbot:", answer)

    except Exception as error:
        print("Error connecting to Ollama:", error)
        conversation_history.pop()
        continue

    # Add assistant response to history for contextual answers
    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    # Save both messages to chat_history.csv
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, session_id, "User", user_input])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id,
            "Chatbot",
            answer
        ])

    # Save chatbot responses separately
    with open(RESPONSES_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id,
            "Chatbot",
            answer
        ])

    # Save readable text logs
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] You: {user_input}\n")
        file.write(f"Chatbot: {answer}\n")
        file.write("-" * 60 + "\n")

print("\nConversation saved successfully.")
print("Chat history:", HISTORY_FILE)
print("Responses:", RESPONSES_FILE)
print("Logs:", LOG_FILE)