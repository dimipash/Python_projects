import os
from typing import Annotated, Dict
from contextlib import contextmanager
from threading import Lock
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field
import ollama

# Load environment variables first
load_dotenv()

class AppConfig(BaseModel):
    """Application configuration settings"""
    api_keys: Dict[str, int] = Field(
        default_factory=lambda: {os.getenv("API_KEY"): 10},
        description="API keys with remaining credits"
    )
    model_name: str = "deepseek-r1:1.5b"
    max_prompt_length: int = 500

class APICreditsManager:
    """Thread-safe API credit management"""
    def __init__(self, initial_credits: Dict[str, int]):
        self.credits = initial_credits
        self.lock = Lock()

    @contextmanager
    def use_credit(self, api_key: str):
        """Context manager for safe credit deduction"""
        with self.lock:
            if self.credits.get(api_key, 0) <= 0:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No credits remaining for this API key"
                )
            self.credits[api_key] -= 1
        
        try:
            yield
        except Exception:
            with self.lock:
                self.credits[api_key] += 1  # Revert on error
            raise

class GenerateRequest(BaseModel):
    """Request model for generation endpoint"""
    prompt: str = Field(..., min_length=1, max_length=500)

class GenerateResponse(BaseModel):
    """Response model for generation endpoint"""
    response: str
    remaining_credits: int

app = FastAPI(title="LLM API Service", version="0.1.0")
config = AppConfig()
credits_manager = APICreditsManager(config.api_keys)

def get_api_key(x_api_key: Annotated[str, Header()]) -> str:
    """Dependency to validate API key header"""
    if x_api_key not in credits_manager.credits:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return x_api_key

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(
    request: GenerateRequest,
    api_key: Annotated[str, Depends(get_api_key)]
) -> GenerateResponse:
    """
    Generate text using the LLM model
    
    Args:
        request: Generation request containing prompt
        api_key: Validated API key from header
    
    Returns:
        Generated response with remaining credits
    """
    with credits_manager.use_credit(api_key):
        try:
            response = ollama.chat(
                model=config.model_name,
                messages=[{"role": "user", "content": request.prompt}]
            )
            return GenerateResponse(
                response=response["message"]["content"],
                remaining_credits=credits_manager.credits[api_key]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model service error: {str(e)}"
            )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv
