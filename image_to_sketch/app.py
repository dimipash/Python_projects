import cv2
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def convert_to_sketch(image_path: str, intensity: int, detail_level: int) -> np.ndarray:
    """Convert an image to a pencil sketch.

    Args:
        image_path (str): Path to the input image.
        intensity (int): Intensity of the sketch (1-10).
        detail_level (int): Detail level of the sketch (1-10).

    Returns:
        np.ndarray: The resulting pencil sketch image.
    """
    img = cv2.imread(image_path)
    if img is None:
        logging.error(
            f"Error loading image from {image_path}. Please check the file path."
        )
        raise FileNotFoundError(f"Image not found at {image_path}")

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blur_level = max(1, intensity) * 3
    blurred_image = cv2.GaussianBlur(inverted_image, (blur_level, blur_level), 0)
    sketch = cv2.divide(gray_image, 255 - blurred_image, scale=255)

    return sketch


def save_image(output_path: str, image: np.ndarray) -> None:
    """Save the processed image to a file.

    Args:
        output_path (str): Path to save the output image.
        image (np.ndarray): The image to save.
    """
    success = cv2.imwrite(output_path, image)
    if not success:
        logging.error(f"Error saving image to {output_path}.")
        raise IOError(f"Could not save image at {output_path}")


def main():
    """Main function to prompt user for input and process images."""

    # Prompt for input image path
    input_file = input("Please enter the path to the input image: ").strip()

    # Prompt for output image path
    output_file = input(
        "Please enter the path where you want to save the output image: "
    ).strip()

    # Prompt for sketch intensity
    while True:
        try:
            intensity = int(input("Enter sketch intensity (1-10): "))
            if 1 <= intensity <= 10:
                break
            else:
                print("Intensity must be between 1 and 10. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 10.")

    # Prompt for sketch detail level
    while True:
        try:
            detail_level = int(input("Enter sketch detail level (1-10): "))
            if 1 <= detail_level <= 10:
                break
            else:
                print("Detail level must be between 1 and 10. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 10.")

    try:
        logging.info("Starting conversion...")
        sketch_image = convert_to_sketch(input_file, intensity, detail_level)

        logging.info("Saving output...")
        save_image(output_file, sketch_image)

        print("Conversion completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
