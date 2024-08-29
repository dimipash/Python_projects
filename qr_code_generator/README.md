![Screenshot](https://github.com/dimipash/Python_projects/blob/main/qr_code_generator/screenshot.jpg)

# QR Code Generator

A simple Python application that generates QR codes from user-provided links using a graphical user interface.

## Features

- Generate QR codes from URLs
- Custom naming for generated QR code files
- Display generated QR code within the application
- User-friendly GUI built with Tkinter

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Required Python libraries:
  - tkinter
  - pyqrcode
  - pillow (PIL)

## Installation

1. Clone this repository.

2. Navigate to the project directory.

3. Install the required dependencies:
   ```
   pip install pyqrcode pillow
   ```

## Usage

1. Run the script.
2. Enter a name for your QR code in the "Link name" field.
3. Enter the URL you want to encode in the "Link" field.
4. Click the "Generate QR Code" button.
5. The generated QR code will be displayed in the application window and saved as a PNG file in the same directory.

## Acknowledgements

- [pyqrcode](https://github.com/mnooner256/pyqrcode) - Python QR Code generator
- [pillow](https://python-pillow.org/) - Python Imaging Library
