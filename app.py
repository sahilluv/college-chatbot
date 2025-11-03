import google.generativeai as genai
import os

# Set your API key here
genai.configure(api_key="AIzaSyDU3-u3xnyLePKswl_GOujIarpahuf_cJk")

# List available models
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {str(e)}")

# Configure the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel("gemini-pro-latest")

print("AI College Chatbot Started! Type 'exit' to stop 👋")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye 👋")
        break
    
    try:
        response = model.generate_content(user_input)
        print("Chatbot:", response.text)
    except Exception as e:
        print(f"Chatbot Error: {str(e)}")  # This will show us the actual error
