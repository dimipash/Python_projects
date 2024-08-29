# Compressing Files Project

This project provides a simple file compression and decompression tool using Python. It includes both command-line and graphical user interface implementations.

## Features

- Compress and decompress text files
- Command-line interface
- Two graphical user interfaces (GUI) for ease of use
- Uses zlib for compression and base64 for encoding

## Files

- `compress_module.py`: Core module with compression and decompression functions
- `compress.py`: Simple command-line implementation
- `gui.py`: Basic GUI implementation
- `gui_any_file.py`: Advanced GUI with file dialog

## Requirements

- Python 3.x
- tkinter (usually comes pre-installed with Python)

## Usage

### Command-line Interface

Run `compress.py` to compress a file named `demo.txt` and create a compressed file named `compressed.txt`.

```
python compress.py
```

### Basic GUI

Run `gui.py` to open a simple graphical interface:

```
python gui.py
```

1. Enter the input file path
2. Enter the output file path
3. Click "Compress" or "Decompress" as needed

### Advanced GUI

Run `gui_any_file.py` for a more user-friendly interface with file dialogs:

```
python gui_any_file.py
```

1. Click "Compress" or "Decompress"
2. Select the input file using the file dialog
3. Enter the output file name
4. The operation will be performed automatically

## How It Works

The compression process uses zlib to compress the data and base64 to encode it into a text format. The decompression process reverses these steps.
