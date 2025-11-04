import google.generativeai as genai
import os

# Set your API key here
genai.configure(api_key="AIzaSyDU3-u3xnyLePKswl_GOujIarpahuf_cJk")

model = genai.GenerativeModel("gemini-1.5-flash-latest")

print("AI College Chatbot Started! Type 'exit' to stop 👋")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye 👋")
        break
    
    response = model.generate_content(user_input)
    print("Chatbot:", response.text)
