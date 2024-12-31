import os
import requests
import pygame
from dotenv import load_dotenv
from pyht import Client
from pyht.client import TTSOptions

# Load environment variables
load_dotenv()

class VoiceCloner:
    def __init__(self):
        self.client = Client(
            user_id=os.getenv("USER_ID"),
            api_key=os.getenv("API_KEY")
        )
        self.headers = {
            "accept": "application/json",
            "AUTHORIZATION": os.getenv("AUTH_TOKEN"),
            "X-USER-ID": os.getenv("X_USER_ID")
        }
        self.base_url = "https://api.play.ht/api/v2/cloned-voices"
        pygame.mixer.init()

    def get_cloned_voices(self):
        try:
            print("\nFetching available voices...")
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            voices = response.json()
            if not voices:
                print("No voices found. Please check your credentials.")
                return None
            return voices
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching cloned voices: {e}")
            return None

    def select_voice(self, voices):
        print("\nAvailable voices:")
        for i, voice in enumerate(voices, 1):
            print(f"{i}. {voice['name']} ({voice['id']})")
        
        while True:
            try:
                choice = int(input("\nSelect a voice (number): "))
                if 1 <= choice <= len(voices):
                    return voices[choice - 1]['id']
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def generate_audio(self, text, voice, output_file="output.wav"):
        try:
            options = TTSOptions(voice=voice)
            with open(output_file, "wb") as audio_file:
                for chunk in self.client.tts(text, options, voice_engine='PlayDialog-http'):
                    audio_file.write(chunk)
            print(f"Audio saved as {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None

    def play_audio(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {e}")

    def cleanup(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file: {e}")

if __name__ == "__main__":
    print("Voice Cloner - Text to Speech with Cloned Voices")
    print("-----------------------------------------------")
    
    cloner = VoiceCloner()
    
    # Get available voices
    voices = cloner.get_cloned_voices()
    if not voices:
        exit(1)
        
    # Select voice
    selected_voice = cloner.select_voice(voices)
    
    # Get user input
    while True:
        text = input("\nEnter the text you want to convert to speech (or 'q' to quit): ")
        if text.lower() == 'q':
            print("\nExiting...")
            break
            
        if not text.strip():
            print("Please enter some text.")
            continue
            
        # Generate and play audio
        output_file = "output.wav"
        print("\nGenerating audio...")
        if cloner.generate_audio(text, selected_voice, output_file=output_file):
            print("Playing audio...")
            cloner.play_audio(output_file)
            cloner.cleanup(output_file)
