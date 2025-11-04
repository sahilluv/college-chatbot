# College Chatbot using Gemini AI

A Python-based chatbot that uses Google's Gemini AI to provide intelligent responses. This chatbot is designed to assist with college-related queries and general conversations.

## Features

- Interactive command-line interface
- Powered by Google's Gemini Pro API
- Environment variable support for secure API key management
- Configurable model parameters
- Error handling for robust operation
 - Help command and simple built-in FAQ
 - Conversation logging: save transcripts to timestamped files in `logs/`
 - Emoji replies: the bot appends a context-aware emoji to responses (type normal messages; emoji is chosen by simple keyword heuristics)

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Required Packages

```bash
google-generativeai==0.8.5
python-dotenv
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sahilluv/college-chatbot.git
   cd college-chatbot
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install google-generativeai python-dotenv
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Make sure your virtual environment is activated
2. Run the chatbot:
   ```bash
   python app.py
   ```
3. Start chatting with the bot
4. Type 'exit' to end the conversation

## Configuration

The chatbot uses the following configuration:
- Temperature: 0.7 (controls response creativity)
- Top-p: 0.8 (nucleus sampling parameter)
- Top-k: 40 (number of tokens to consider)
- Max output tokens: 2048

## Security Notes

- Never commit your `.env` file
- The `.gitignore` file is set up to exclude sensitive information
- Always use environment variables for API keys

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.