# Python AI Mentor

A voice-enabled Python programming mentor powered by DeepSeek's LLM and Replicate's text-to-speech.

## Features
- Interactive Python coding guidance
- Natural language voice responses
- Environment configuration validation
- Error handling and graceful recovery
- Cross-platform compatibility

## Prerequisites
- Python 3.9+
- [Replicate API Token](https://replicate.com/)
- [DeepSeek API Key](https://platform.deepseek.com/)

## Installation
```bash
clone this repo
cd python-mentor
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
1. Create `.env` file:
```env
REPLICATE_API_TOKEN="your_replicate_token"
DEEPSEEK_API_KEY="your_deepseek_key"
```

2. Configure voice settings in `main.py`:
```python
VOICE = "af_bella"  # Choose from available voices
AUDIO_OUTPUT_FILE = "output.wav"  # Change output format if needed
```

## Usage
```bash
python main.py
```

## Troubleshooting
- **Audio playback issues:** Ensure system audio drivers are updated
- **API errors:** Verify tokens in `.env` and check provider status pages
- **Environment issues:** Recreate virtual environment if dependency conflicts occur

## License
MIT License

## Contributing
Pull requests welcome! Please maintain PEP8 style and include tests for new features.
