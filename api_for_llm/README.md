# Ollama Text Generation API

## Overview
This is a FastAPI-based microservice for text generation using Ollama models with API key authentication and credit-based access control.

## Features
- Text generation using Ollama models
- API key authentication
- Credit-based access management
- Logging and error handling

## Prerequisites
- Python 3.8+
- pip
- Ollama installed and configured

## Installation

1. Clone this repository:

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your API keys:
```
API_KEYS=key1,key2,key3
```
- Each API key is initialized with 5 credits
- Credits are consumed with each text generation request

## Running the Application

### Development Server
```bash
uvicorn main:app --reload
```

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /generate
Generate text using an Ollama model

#### Request Body
```json
{
    "prompt": "Your text generation prompt",
    "model": "deepseek-r1:1.5b"  // Optional, defaults to deepseek-r1:1.5b
}
```

#### Headers
- `x-api-key`: Your API key

#### Response
```json
{
    "response": "Generated text content"
}
```

## Error Handling
- 401: Invalid or exhausted API key
- 500: Internal server error during text generation

## Logging
Logs are output to the console with timestamp, log level, and message.



