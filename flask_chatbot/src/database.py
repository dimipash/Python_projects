import sqlite3
from datetime import datetime

class ChatDatabase:
    def __init__(self, db_file="chat_history.db"):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_conversation(self, user_message, bot_response):
        """Save a conversation exchange to the database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_message, bot_response, timestamp)
            VALUES (?, ?, ?)
        ''', (user_message, bot_response, datetime.now()))
        
        conn.commit()
        conn.close()

    def get_chat_history(self, limit=50):
        """Retrieve recent chat history"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, bot_response, timestamp
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        history = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries and reverse to show oldest first
        formatted_history = [
            {
                'user_message': msg,
                'bot_response': resp,
                'timestamp': ts
            } for msg, resp, ts in reversed(history)
        ]
        
        return formatted_history 