from typing import Dict, Any, Optional
import yaml
import argparse
import logging
from pathlib import Path
from functools import wraps
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers.utils.logging import set_verbosity_error

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
set_verbosity_error()

class ModelManager:
    """Manages model loading and configuration"""
    
    def __init__(self, config_path: str = "config.yml"):
        self.config = self._load_config(config_path)
        self.models = self._initialize_models()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise RuntimeError("Configuration error") from e
            
    def _initialize_models(self) -> Dict[str, Any]:
        """Initialize all models from config"""
        models_config = self.config["models"]
        return {
            "summarizer": self._create_pipeline(
                task="summarization",
                model=models_config["summarization"]["base_model"],
                device=models_config["summarization"]["device"]
            ),
            "refiner": self._create_pipeline(
                task="summarization",
                model=models_config["summarization"]["refinement_model"],
                device=models_config["summarization"]["device"]
            ),
            "qa": self._create_pipeline(
                task="question-answering",
                model=models_config["summarization"]["qa_model"],
                device=models_config["summarization"]["device"]
            )
        }
        
    def _create_pipeline(self, task: str, model: str, device: int) -> HuggingFacePipeline:
        """Create a HuggingFace pipeline with validation"""
        try:
            pipe = pipeline(
                task=task,
                model=model,
                device=device,
                max_length=self.config["system"]["max_summary_length"]
            )
            return HuggingFacePipeline(pipeline=pipe)
        except Exception as e:
            logger.error(f"Model loading failed for {model}: {e}")
            raise

def handle_errors(func):
    """Decorator for error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

@handle_errors
def main():
    # Initialize system components
    model_mgr = ModelManager()
    parser = argparse.ArgumentParser(description="Text Summarization and QA System")
    
    # Configure CLI arguments
    parser.add_argument("--text", type=str, help="Text to summarize")
    parser.add_argument("--length", type=str, default="medium",
                      choices=["short", "medium", "long"],
                      help="Summary length")
    parser.add_argument("--interactive", action="store_true",
                      help="Enable interactive Q&A mode")
    
    args = parser.parse_args()
    
    # Validate input
    if len(args.text) > model_mgr.config["system"]["max_input_length"]:
        raise ValueError("Input text exceeds maximum allowed length")
        
    # Create processing chain
    summary_template = PromptTemplate.from_template(
        "Summarize the following text in a {length} way:\n\n{text}"
    )
    summarization_chain = (
        summary_template 
        | model_mgr.models["summarizer"] 
        | model_mgr.models["refiner"]
    )
    
    # Generate summary
    summary = summarization_chain.invoke({
        "text": args.text,
        "length": args.length
    })
    
    print("\n🔹 **Generated Summary:**")
    print(summary)
    
    # Interactive Q&A
    if args.interactive:
        while True:
            try:
                question = input("\nAsk a question about the summary (or 'exit'):\n")
                if question.lower() == "exit":
                    break
                    
                qa_result = model_mgr.models["qa"](
                    question=question,
                    context=summary
                )
                
                print("\n🔹 **Answer:**")
                print(qa_result["answer"])
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
