import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

"""
Local LLM Chatbot

This script implements a chatbot using a local language model (LLM) via the Ollama library.
It maintains a conversation history and allows users to interact with the AI in a 
command-line interface.

Features:
- Uses Ollama for local LLM inference
- Maintains conversation history
- Allows clearing of conversation history
- Truncates context to prevent exceeding token limits

Usage:
Run the script and interact with the chatbot via the command line.
Type 'exit' to quit the program or 'clear' to start a new conversation.

"""

# Configuration
MODEL_NAME = "llama3.1"
MAX_CONTEXT_LENGTH = 2000


def create_llm():
    return OllamaLLM(model=MODEL_NAME)


def create_prompt():
    template = """
    You are a helpful AI assistant. Answer the question based on the conversation history and current query.

    Conversation history:
    {history}

    Human: {input}
    AI Assistant:
    """
    return ChatPromptTemplate.from_template(template)


def create_runnable_chain(llm, prompt):
    chain = (
        RunnablePassthrough.assign(history=lambda x: x["history"])
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def truncate_context(context, max_length):
    while len(context) > max_length:
        context.pop(0)
    return context


def handle_conversation():
    llm = create_llm()
    prompt = create_prompt()
    chain = create_runnable_chain(llm, prompt)

    print(
        "Welcome to the AI ChatBot. Type 'exit' to quit, 'clear' to start a new conversation."
    )

    history = []
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "clear":
            history = []
            print("Conversation history cleared.")
            continue

        history_text = "\n".join(history)
        response = chain.invoke({"input": user_input, "history": history_text})
        print("Bot:", response)

        history.append(f"Human: {user_input}")
        history.append(f"AI: {response}")
        history = truncate_context(history, MAX_CONTEXT_LENGTH)


if __name__ == "__main__":
    handle_conversation()
