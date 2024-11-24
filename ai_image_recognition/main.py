import ollama
import argparse
import os
from typing import List
from PIL import Image


def validate_image(image_path: str) -> bool:
    """Validate if the file exists and is a valid image."""
    try:
        if not os.path.exists(image_path):
            return False
        Image.open(image_path)
        return True
    except Exception:
        return False


def process_images(image_paths: List[str], model: str = "llava:7b") -> str:
    """Process multiple images and get AI descriptions."""
    # Validate images first
    valid_images = []
    for img_path in image_paths:
        if validate_image(img_path):
            valid_images.append(img_path)
        else:
            print(f"Warning: Skipping invalid image: {img_path}")

    if not valid_images:
        raise ValueError("No valid images provided")

    try:
        res = ollama.chat(
            model=model,
            message=[
                {
                    "role": "user",
                    "content": "Describe these images in detail",
                    "images": valid_images,
                }
            ],
        )
        return res["message"]["content"]
    except Exception as e:
        raise Exception(f"Error processing images: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="AI Image Recognition Tool")
    parser.add_argument("images", nargs="+", help="Paths to image files")
    parser.add_argument("--model", default="llava:7b", help="AI model to use")

    args = parser.parse_args()

    try:
        result = process_images(args.images, args.model)
        print("\n=== AI Image Description ===")
        print(result)
        print("=========================\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
