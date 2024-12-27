# Image to Sketch Converter

This Python script, `app.py`, converts an image to a pencil sketch. It prompts the user for the input image path, desired output path, sketch intensity, and detail level.

## Features

- Converts color images to grayscale pencil sketches.
- Allows customization of sketch intensity and detail level.
- Handles basic error checking for image loading and saving.

## Prerequisites

- Python 3.x
- OpenCV library (`cv2`)
- NumPy library (`numpy`)

You can install the necessary dependencies using pip:

```bash
pip install opencv-python numpy
```

## Usage

1. Save the `app.py` script to your desired location.
2. Open a terminal or command prompt and navigate to the directory where you saved `app.py`.
3. Run the script using the Python interpreter:

    ```bash
    python app.py
    ```

4. The script will then prompt you for the following information:
    - **Input image path:** The path to the image you want to convert.
    - **Output image path:** The path where you want to save the resulting sketch image.
    - **Sketch intensity (1-10):**  Controls the blur level applied to the inverted image, affecting the thickness of the sketch lines. Higher values result in thicker lines.
    - **Sketch detail level (1-10):** This parameter is currently not used in the image processing logic but is requested by the script.

## Example

```
Please enter the path to the input image: input.jpeg
Please enter the path where you want to save the output image: output_sketch.png
Enter sketch intensity (1-10): 5
Enter sketch detail level (1-10): 7
```

After running the script, a new image file (e.g., `output_sketch.png`) will be created in the specified output path containing the pencil sketch of the input image.

## Error Handling

The script includes basic error handling:

- If the input image file is not found, an error message will be logged and displayed.
- If there is an issue saving the output image, an error message will be logged and displayed.
- If the user provides invalid input for intensity or detail level, the script will prompt them to enter a valid integer within the specified range.

## Logging

The script uses the `logging` module to record informational messages and errors. Log messages are printed to the console.

## Functionality Breakdown

- `convert_to_sketch(image_path: str, intensity: int, detail_level: int) -> np.ndarray`: This function takes the path to an image, an intensity level, and a detail level as input. It reads the image, converts it to grayscale, inverts it, applies a Gaussian blur based on the intensity, and then uses a division blend to create the sketch effect. The detail level parameter is currently not utilized in the image processing.
- `save_image(output_path: str, image: np.ndarray) -> None`: This function saves the provided image to the specified output path.
- `main()`: This is the main function that handles user input, calls the image processing functions, and prints the results.
