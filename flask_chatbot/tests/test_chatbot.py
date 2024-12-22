import unittest
import json
import os
from src.chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create test responses file
        self.test_responses = {
            "hello": "Hi there!",
            "test question": "test answer",
            "how are you": "I'm good!"
        }
        
        os.makedirs('tests/test_data', exist_ok=True)
        with open('tests/test_data/test_responses.json', 'w') as f:
            json.dump(self.test_responses, f)
            
        self.chatbot = Chatbot()
        self.chatbot.responses = self.test_responses

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove('tests/test_data/test_responses.json')
            os.rmdir('tests/test_data')
        except:
            pass

    def test_preprocess_input(self):
        """Test input preprocessing"""
        test_cases = [
            ("Hello!", "hello"),
            ("How ARE you?", "how are you"),
            ("Test@#$%^&*", "test"),
            ("   spaces   ", "spaces")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.chatbot.preprocess_input(input_text)
                self.assertEqual(result, expected)

    def test_find_best_match(self):
        """Test fuzzy matching functionality"""
        test_cases = [
            ("hello there", "hello"),
            ("how r u", "how are you"),
            ("completely random", None)
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.chatbot.find_best_match(input_text, self.test_responses.keys())
                self.assertEqual(result, expected)

    def test_get_response(self):
        """Test response generation"""
        # Test exact match
        response = self.chatbot.get_response("hello")
        self.assertEqual(response, "Hi there!")
        
        # Test fuzzy match
        response = self.chatbot.get_response("hello there")
        self.assertEqual(response, "Hi there!")
        
        # Test no match
        response = self.chatbot.get_response("xyzabc")
        self.assertEqual(response, "I'm sorry, I don't understand that. Could you rephrase?")

    def test_conversation_history(self):
        """Test conversation history tracking"""
        test_input = "hello"
        self.chatbot.get_response(test_input)
        
        # Check if conversation history is being recorded
        self.assertEqual(len(self.chatbot.conversation_history), 2)  # User input + bot response
        self.assertEqual(self.chatbot.conversation_history[0]["user"], test_input)
        self.assertEqual(self.chatbot.conversation_history[1]["bot"], "Hi there!")

if __name__ == '__main__':
    unittest.main()
