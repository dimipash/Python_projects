import os
from dotenv import load_dotenv
from openai import OpenAI
import replicate
from playsound3 import playsound
from typing import List, Dict

# Constants
MODEL_NAME = "deepseek-reasoner"
REPLICATE_MODEL = "jaaari/kokoro-82m:dfdf537ba482b029e0a761699e6f55e9162cfd159270bfe0e44857caa5f275a6"
VOICE = "af_bella"
AUDIO_OUTPUT_FILE = "output.wav"

# Load environment variables
load_dotenv()

# Initialize clients
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """\
You are a friendly and polite Python mentor. \
You use easy-to-understand language and provide brief, practical examples. \
You help students by examining issues and offering concise solutions. \
Your answers focus on Python best practices and real-world applications.\
"""

def chat() -> None:
    """Main chat loop with the Python mentor AI."""
    history: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Start chatting with your Python mentor (type 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                break
                
            history.append({"role": "user", "content": user_input})
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=history,
                stream=False,
            )
            
            answer = response.choices[0].message.content
            history.append({"role": "assistant", "content": answer})
            
            print(f"\nMentor: {answer}\n")
            say(answer)
            
        except KeyboardInterrupt:
            print("\n\nExiting chat...")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

def say(text: str) -> None:
    """Convert text to speech using Replicate's API and play it."""
    try:
        print("\nGenerating audio response...")
        output = replicate.run(
            REPLICATE_MODEL,
            input={
                "text": text,
                "speed": 1.1,
                "voice": VOICE
            }
        )
        
        with open(AUDIO_OUTPUT_FILE, "wb") as f:
            f.write(output.read())
            
        playsound(AUDIO_OUTPUT_FILE)
        print("Audio playback completed.\n")
        
    except Exception as e:
        print(f"Audio error: {e}")

if __name__ == "__main__":
    # Verify environment setup
    required_vars = {
        "REPLICATE_API_TOKEN": os.getenv("REPLICATE_API_TOKEN"),
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY")
    }
    
    if all(required_vars.values()):
        print("System check passed. Starting mentor session...\n")
        chat()
    else:
        missing = [k for k, v in required_vars.items() if not v]
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Please check your .env file and try again.")
