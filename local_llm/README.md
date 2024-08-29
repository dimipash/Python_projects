# AI ChatBot

An interactive AI-powered chatbot built with Python, leveraging the LangChain library and Ollama LLM.

## Features

- Conversational AI interface using the LLama 3.1 model
- Context-aware responses based on conversation history
- Easy-to-use command-line interface
- Ability to clear conversation history
- Automatic context truncation to manage token limits

## Requirements

- Python 3.7+
- langchain_ollama
- langchain_core

## Installation

1. Clone this repository.

2. Install the required dependencies:

   ```
   pip install langchain_ollama langchain_core
   ```

3. Ensure you have Ollama installed and the LLama 3.1 model available.

## Usage

Run the chatbot with the following command:

```
python main.py
```

- Type your messages and press Enter to interact with the AI.
- Type 'exit' to quit the application.
- Type 'clear' to start a new conversation by clearing the history.

## Configuration

You can modify the following variables in the script to customize the chatbot:

- `MODEL_NAME`: The name of the Ollama model to use (default: "llama3.1")
- `MAX_CONTEXT_LENGTH`: The maximum length of the conversation history to maintain (default: 2000)

## How It Works

1. The script initializes an Ollama LLM instance with the specified model.
2. It creates a prompt template for the AI assistant.
3. A runnable chain is set up to process user input and conversation history.
4. The main loop handles user input, sends it to the AI model, and displays the response.
5. Conversation history is maintained and truncated as needed to manage context length.
