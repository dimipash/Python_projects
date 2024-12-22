from src.chatbot import Chatbot

def main():
    print("PyBot: Hello! I'm PyBot. Type 'quit' to exit.")
    chatbot = Chatbot()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("PyBot: Goodbye!")
            break
            
        try:
            response = chatbot.get_response(user_input)
            print(f"PyBot: {response}")
        except Exception as e:
            print(f"PyBot: Sorry, I encountered an error: {str(e)}")

if __name__ == "__main__":
    main()
