# Desktop Cleanup Script

## Description

This Python script automatically organizes files on your desktop by moving them into category-specific folders based on their file extensions. It helps maintain a clean and organized desktop environment.

## Features

- Automatically creates category folders on the desktop if they don't exist
- Sorts files into appropriate folders based on their extensions
- Handles a wide variety of file types including:
  - Images
  - Documents
  - Spreadsheets
  - Presentations
  - Audio files
  - Video files
  - Archives
  - Code files
  - Executables
  - Fonts
  - eBooks
  - Vector graphics
  - 3D models
  - Data files
- Moves unsorted files to an "Others" folder

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository or download the script file.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

Run the script from the command line:

```
python desktop_cleanup.py
```

The script will automatically organize the files on your desktop.

## How it works

1. The script identifies the user's desktop directory.
2. It creates category folders if they don't already exist.
3. It iterates through all files on the desktop.
4. For each file, it determines the appropriate category based on the file extension.
5. It moves the file to the corresponding category folder.
6. Files with unrecognized extensions are moved to the "Others" folder.

## Customization

You can easily customize the script by modifying the `folders` dictionary in the `clean_desktop()` function. Add or remove categories and file extensions as needed.

## Caution

- Always backup your important files before running cleanup scripts.
- The script moves files without asking for confirmation. Make sure you're comfortable with automatic file organization before running it.
