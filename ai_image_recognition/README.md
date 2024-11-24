# AI Image Recognition Tool

A Python-based command-line tool that uses AI to generate detailed descriptions of images using the Ollama API and the LLaVA model.

## Features

- Process multiple images simultaneously
- Support for different AI models through Ollama
- Detailed image descriptions using state-of-the-art AI
- Input validation and error handling
- Command-line interface for easy use

## Requirements

- Python 3.6+
- Ollama
- PIL (Python Imaging Library)
- argparse

1. Clone this repository:

2. Install the required dependencies:

```bash
pip install ollama-python Pillow
```

3. Make sure you have Ollama installed and running with the LLaVA model:

```bash
ollama pull llava:7b
```

## Usage

Basic usage:

```bash
python main.py path/to/image1.jpg path/to/image2.jpg
```

Using a different model:

```bash
python main.py path/to/image.jpg --model "llava:13b"
```

## How It Works

The tool performs the following steps:

1. Validates input images to ensure they exist and are valid image files
2. Processes images using the specified AI model (default: llava:7b)
3. Returns detailed descriptions of the images

## Error Handling

The tool includes robust error handling for:

- Invalid image files
- Missing files
- API errors
- Invalid model specifications

## Example Output

```
=== AI Image Description ===
[Detailed AI-generated description of your images will appear here]
=========================
```

