# Text-to-Speech Project

This project demonstrates various ways to implement text-to-speech functionality using Python and the gTTS (Google Text-to-Speech) library.

## Files

1. `demo.py`: A simple script that converts a hardcoded text to speech.
2. `file_data_to_audio.py`: A script that reads text from a file and converts it to speech.
3. `gui.py`: A graphical user interface for text-to-speech conversion.

## Requirements

- Python 3.x
- gTTS library
- tkinter (for GUI)

To install the required library, run:

```
pip install gtts
```

## Usage

### demo.py

This script converts the text "Hello World!" to speech and saves it as an MP3 file.

To run:

```
python demo.py
```

### file_data_to_audio.py

This script reads text from a file named 'demo.txt' and converts it to speech.

1. Create a file named 'demo.txt' with the text you want to convert.
2. Run the script:

```
python file_data_to_audio.py
```

### gui.py

This script provides a graphical interface for text-to-speech conversion.

To run:

```
python gui.py
```

Enter your text in the input field and click "Start" to convert it to speech.
