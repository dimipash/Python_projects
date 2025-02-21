import logging
from typing import Dict, Optional

import ollama
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class APIKeyManager:
    """
    Manages API keys and their associated credits.
    
    This class provides a simple in-memory credit tracking system 
    for API key authentication and usage.
    """
    def __init__(self):
        # Load API keys from environment variable
        api_keys_str = os.getenv("API_KEYS", "")
        self.api_key_credits: Dict[str, int] = {
            key.strip(): 5 for key in api_keys_str.split(',') if key.strip()
        }
        logger.info(f"Initialized API keys: {list(self.api_key_credits.keys())}")

    def verify_api_key(self, api_key: Optional[str]) -> str:
        """
        Verify and validate the API key.
        
        Args:
            api_key (str): The API key to verify.
        
        Raises:
            HTTPException: If the API key is invalid or has no credits.
        
        Returns:
            str: The validated API key.
        """
        if not api_key:
            logger.warning("No API key provided")
            raise HTTPException(status_code=401, detail="API key is required")
        
        credits = self.api_key_credits.get(api_key, 0)
        if credits <= 0:
            logger.warning(f"Invalid or exhausted API key: {api_key}")
            raise HTTPException(status_code=401, detail="Invalid API Key or no credits remaining")
        
        return api_key

    def consume_credit(self, api_key: str) -> None:
        """
        Consume a credit for the given API key.
        
        Args:
            api_key (str): The API key to consume credit for.
        """
        if api_key in self.api_key_credits:
            self.api_key_credits[api_key] -= 1
            logger.info(f"Credit consumed for API key. Remaining: {self.api_key_credits[api_key]}")

class GenerateRequest(BaseModel):
    """
    Pydantic model for generate endpoint request.
    """
    prompt: str
    model: str = "deepseek-r1:1.5b"

# Initialize API key manager
api_key_manager = APIKeyManager()

# Create FastAPI app
app = FastAPI(
    title="Ollama Text Generation API",
    description="API for generating text using Ollama models with API key authentication",
    version="0.1.0"
)

@app.post("/generate")
def generate(
    request: GenerateRequest, 
    x_api_key: str = Depends(api_key_manager.verify_api_key)
):
    """
    Generate text based on the provided prompt.
    
    Args:
        request (GenerateRequest): The generation request containing prompt and model.
        x_api_key (str): The API key for authentication.
    
    Returns:
        dict: Generated text response.
    """
    try:
        # Consume API key credit
        api_key_manager.consume_credit(x_api_key)
        
        # Generate text using Ollama
        response = ollama.chat(
            model=request.model, 
            messages=[{"role": "user", "content": request.prompt}]
        )
        
        logger.info(f"Text generation successful for model: {request.model}")
        return {"response": response["message"]["content"]}
    
    except Exception as e:
        logger.error(f"Error during text generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during text generation")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
