# Voice Cloner

A Python application for cloning voices using the Play.ht API.

## Features
- Convert text to speech using cloned voices
- Interactive voice selection
- Audio playback
- Automatic cleanup of generated files

## Requirements
- Python 3.8+
- Play.ht API credentials

## Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your credentials:
   ```
   USER_ID=your_user_id
   API_KEY=your_api_key
   AUTH_TOKEN=your_auth_token
   X_USER_ID=your_x_user_id
   ```

## Usage
Run the application:
```bash
python app.py
```

Follow the on-screen prompts to:
1. Select a voice
2. Enter text to convert
3. Listen to the generated audio

The application will automatically clean up generated files after playback.

## License
MIT
