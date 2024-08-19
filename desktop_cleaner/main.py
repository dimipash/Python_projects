import os
import shutil
from pathlib import Path


def clean_desktop():
    # Get the path to the desktop
    desktop = Path.home() / "Desktop"

    # Create folders for different file types
    folders = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".tex"],
        "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
        "Presentations": [".ppt", ".pptx", ".key", ".odp"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Code": [
            ".py",
            ".java",
            ".cpp",
            ".c",
            ".html",
            ".css",
            ".js",
            ".php",
            ".rb",
            ".swift",
        ],
        "Executables": [".exe", ".msi", ".app", ".dmg"],
        "Font": [".ttf", ".otf", ".woff", ".woff2"],
        "eBooks": [".epub", ".mobi", ".azw", ".azw3"],
        "Vector Graphics": [".svg", ".ai", ".eps"],
        "3D Models": [".obj", ".stl", ".fbx", ".blend"],
        "Data": [".json", ".xml", ".yaml", ".sql", ".db"],
        "Shortcuts": [],
    }

    # Create the folders if they don't exist
    for folder in folders:
        folder_path = desktop / folder
        folder_path.mkdir(exist_ok=True)

    # Move files to appropriate folders
    for item in desktop.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower()
            destination_folder = "Others"

            for folder, extensions in folders.items():
                if file_ext in extensions:
                    destination_folder = folder
                    break

            destination = desktop / destination_folder / item.name
            shutil.move(str(item), str(destination))

    print("Desktop cleanup completed!")


if __name__ == "__main__":
    clean_desktop()
