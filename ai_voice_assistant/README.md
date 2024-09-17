# Voice Assistant Project

This voice assistant project combines speech recognition, natural language processing, and custom functions to create an interactive, voice-controlled temperature management system.

## Main Components (`main.py`)

-   `VoiceAssistant`: Core class for the voice assistant
-   Plugins:
    -   `silero` (VAD)
    -   `openai` (STT, LLM, TTS)
-   `AssistantFnc`: Custom function context for temperature control

## Entrypoint Function

```python
async def entrypoint(ctx: JobContext):
    # Initializes the voice assistant with necessary components
    # Connects to a room and starts the assistant
    # Greets the user with an initial message
```

## Temperature Control Functions (`api.py`)

-   `AssistantFnc` class: Manages temperature settings for different zones
-   Functions:
    -   `get_temperature`: Retrieves temperature for a specific zone
    -   `set_temperature`: Sets temperature for a specific zone

## Key Features

-   Voice-based interaction
-   Temperature control for multiple zones (living room, bedroom, kitchen, etc.)
-   Integration with OpenAI's language model and text-to-speech

## Usage

1. Run the script to start the voice assistant
2. Interact with the assistant using voice commands
3. Control and query temperatures in different zones

## Code Structure

### `main.py`

```python
import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

# ... (rest of the code)
```

### `api.py`

```python
import enum
from typing import Annotated
from livekit.agents import llm
import logging

# ... (rest of the code)
```
