import json
import re
from difflib import get_close_matches
from src.database import ChatDatabase

class Chatbot:
    def __init__(self):
        self.responses = self._load_responses()
        self.conversation_history = []
        self.db = ChatDatabase()

    def _load_responses(self):
        """Load response data from JSON file"""
        try:
            with open('data/responses.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Response file not found. Using empty responses.")
            return {}

    def preprocess_input(self, user_input):
        """Clean and normalize user input"""
        # Convert to lowercase, remove special characters, and strip whitespace
        cleaned_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip()
        return cleaned_input

    def find_best_match(self, user_input, questions):
        """Find the closest matching question using fuzzy matching"""
        matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_response(self, user_input):
        """Generate a response based on user input"""
        processed_input = self.preprocess_input(user_input)
        
        # Store conversation
        self.conversation_history.append({"user": user_input})
        
        # Find best matching response
        best_match = self.find_best_match(processed_input, self.responses.keys())
        
        if best_match:
            response = self.responses[best_match]
        else:
            response = "I'm sorry, I don't understand that. Could you rephrase?"
        
        # Store bot response
        self.conversation_history.append({"bot": response})
        
        # Save to database
        self.db.save_conversation(user_input, response)
        
        return response
