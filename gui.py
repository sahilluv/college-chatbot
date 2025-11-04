import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime
from pathlib import Path
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Simple model config (mirrors app.py)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel("gemini-pro-latest", generation_config=generation_config)

# Ensure logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Emoji rules
EMOJI_RULES = [
    (r"\b(thank|thanks)\b", "🙏"),
    (r"\b(congrat|congrats|well done|nice job)\b", "🎉"),
    (r"\b(lol|haha|😂)\b", "😂"),
    (r"\b(happy|great|good|awesome|fantastic)\b", "😊"),
    (r"\b(sad|unhappy|depress|down)\b", "😔"),
    (r"\b(angry|mad|furious)\b", "😠"),
    (r"\b(love|❤️|like)\b", "❤️"),
]

def select_emoji(user_text: str, reply_text: str) -> str:
    text = (user_text + " " + (reply_text or "")).lower()
    if user_text.strip().endswith("?"):
        return "🤔"
    for pattern, emoji in EMOJI_RULES:
        if re.search(pattern, text):
            return emoji
    return "😊"

class ChatGUI:
    def __init__(self, root):
        self.root = root
        root.title("College Chatbot — GUI")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=80, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=3, padx=8, pady=8)

        self.entry = tk.Entry(root, width=70)
        self.entry.grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.entry.bind("<Return>", lambda e: self.on_send())

        self.send_btn = tk.Button(root, text="Send", command=self.on_send)
        self.send_btn.grid(row=1, column=1, padx=4, pady=8)

        self.save_btn = tk.Button(root, text="Save", command=self.on_save)
        self.save_btn.grid(row=1, column=2, padx=4, pady=8)

        self.conversation = []

    def append_chat(self, text: str):
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.configure(state=tk.DISABLED)

    def on_send(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self.append_chat(f"You: {user_text}")
        self.conversation.append(f"You: {user_text}")
        # run model call in thread
        threading.Thread(target=self._call_model, args=(user_text,), daemon=True).start()

    def _call_model(self, user_text: str):
        # disable buttons while waiting
        self.send_btn.configure(state=tk.DISABLED)
        self.save_btn.configure(state=tk.DISABLED)
        try:
            response = model.generate_content(
                user_text,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ],
            )
            reply = getattr(response, "text", "")
        except Exception as e:
            reply = f"<error> {e}"

        emoji = select_emoji(user_text, reply)
        final = f"Bot: {reply} {emoji}" if reply else f"Bot: I couldn't generate a response. {emoji}"
        # update UI on main thread
        self.root.after(0, lambda: self.append_chat(final))
        self.conversation.append(final)
        self.root.after(0, lambda: self.send_btn.configure(state=tk.NORMAL))
        self.root.after(0, lambda: self.save_btn.configure(state=tk.NORMAL))

    def on_save(self):
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = LOGS_DIR / f"gui_chat_{ts}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(self.conversation))
            messagebox.showinfo("Saved", f"Conversation saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

def main():
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
