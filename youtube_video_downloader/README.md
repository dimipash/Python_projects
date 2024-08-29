![YouTube Video Downloader](https://github.com/dimipash/Python_projects/blob/main/youtube_video_downloader/screenshot.jpg)

# YouTube Downloader

A simple Python application with a graphical user interface for downloading YouTube videos and extracting audio.

## Features

- Download YouTube videos in highest available resolution
- Extract audio from downloaded videos
- User-friendly GUI built with Tkinter
- Choose custom download location

## Requirements

- Python 3.6+
- tkinter
- pytube
- moviepy

## Installation

1. Clone this repository.

2. Install the required packages:
   ```
   pip install pytube moviepy
   ```

## Usage

1. Run the script:

   ```
   python main.py
   ```

2. Enter the URL of the YouTube video you want to download.

3. Click the "Select" button to choose the download location.

4. Click the "Download" button to start the download process.

5. Wait for the "Download Complete" message in the console.

## How it works

1. The app uses `pytube` to download the YouTube video in its highest available resolution.
2. It then uses `moviepy` to extract the audio from the video and save it as an MP3 file.
3. Both the video and audio files are moved to the user-specified download location.
