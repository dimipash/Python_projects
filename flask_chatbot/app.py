from flask import Flask, render_template, request, jsonify
from src.chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/')
def home():
    # Get chat history from database
    chat_history = chatbot.db.get_chat_history()
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = chatbot.get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
