# Simple Text Editor

A lightweight text editor built with Python and Tkinter. This application provides basic text editing functionality with a clean and intuitive user interface.

## Features

- Open and edit existing text files
- Create new text files
- Save files with custom names and locations
- Simple and user-friendly interface

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository.
2. Navigate to the project directory:
   ```
   cd simple-text-editor
   ```

## Usage

Run the script using Python:

```
python text_editor.py
```

The text editor window will open, allowing you to:

- Click "Open" to browse and open an existing text file
- Edit the content in the main text area
- Click "Save As..." to save your changes or create a new file

## How it works

The application uses Tkinter to create a graphical user interface with the following components:

- A main window with a title "Text Editor"
- A text area for editing content
- "Open" and "Save As..." buttons for file operations

The `open_file()` function allows users to select and open text files, while the `save_file()` function enables saving the current content to a new or existing file.
