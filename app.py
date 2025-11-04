from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime
from pathlib import Path
import json

# Load environment variables from .env file
load_dotenv()

# Configure API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models (helpful for debugging)
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {str(e)}")

# Configure the model with specific parameters for college-related responses
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Initialize the model with configuration
model = genai.GenerativeModel("gemini-pro-latest", generation_config=generation_config)

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# In-memory conversation buffer
conversation = []

# Small hard-coded FAQ mapping (can be expanded)
FAQ = {
    "how to study": "Create a study schedule, use active recall and spaced repetition, and break tasks into focused intervals (Pomodoro).",
    "choose major": "Consider your interests, strengths, job prospects, and talk to advisors and professors before deciding.",
    "time management": "Prioritize tasks, break work into small chunks, use a planner, and eliminate distractions.",
}

HELP_TEXT = (
    "Available commands:\n"
    "- help : Show this help text\n"
    "- save : Save the current conversation to a timestamped file in the logs/ folder\n"
    "- faq: <key> : Ask a built-in FAQ. Example keys: 'how to study', 'choose major', 'time management'\n"
    "- exit : Exit the chatbot\n"
)

print("AI College Chatbot Started! Type 'exit' to stop 👋")

while True:
    user_input = input("You: ")

    # Normalize for simple command parsing
    user_lower = user_input.strip().lower()

    if user_lower == "exit":
        print("Chatbot: Goodbye 👋")
        break

    # Built-in commands
    if user_lower == "help":
        print(HELP_TEXT)
        continue

    if user_lower == "save":
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = LOGS_DIR / f"chat_{ts}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(conversation))
            print(f"Chatbot: Conversation saved to {filename}")
        except Exception as e:
            print(f"Chatbot: Failed to save conversation: {e}")
        continue

    if user_lower.startswith("faq"):
        # Accept either "faq: <key>" or "faq <key>"
        key = user_input.partition(":")[2].strip() or user_input.partition(" ")[2].strip()
        key_lower = key.lower()
        ans = FAQ.get(key_lower)
        if ans:
            print("Chatbot:", ans)
            conversation.append(f"You: {user_input}")
            conversation.append(f"Bot: {ans}")
        else:
            print("Chatbot: I don't have an FAQ answer for that key. Try 'help' to see available commands.")
        continue

    # Append user message to conversation buffer
    conversation.append(f"You: {user_input}")

    # Call the model and handle responses
    try:
        response = model.generate_content(
            user_input,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        )

        reply = getattr(response, "text", None)
        if reply:
            print("Chatbot:", reply)
            conversation.append(f"Bot: {reply}")
        else:
            print("Chatbot: I couldn't generate a response. Try rephrasing your question.")
            conversation.append("Bot: <no response>")

    except Exception as e:
        print(f"Chatbot Error: {str(e)}")
        print("Chatbot: I apologize for the error. Please try again or ask a different question.")
        conversation.append(f"Bot: <error> {str(e)}")
