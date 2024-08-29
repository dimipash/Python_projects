![screenshot](https://github.com/dimipash/Python_projects/tree/main/youtube_audio_downloader/screenshot.png)

# YouTube Audio Downloader

## Description

This Python script allows users to download the audio from YouTube videos in various formats and qualities. It uses the `yt-dlp` library, which is a fork of `youtube-dl` with additional features and fixes.

## Features

- Download audio from YouTube videos
- Customize output filename
- Choose audio codec (mp3, m4a, opus, etc.)
- Set preferred bitrate
- Simple command-line interface

## Requirements

- Python 3.6 or higher
- yt-dlp library
- FFmpeg (for audio conversion)

## Installation

1. Clone this repository or download the script file.
2. Install the required Python library:
   ```
   pip install yt-dlp
   ```
3. Install FFmpeg:
   - On macOS (using Homebrew): `brew install ffmpeg`
   - On Ubuntu or Debian: `sudo apt-get install ffmpeg`
   - On Windows: Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add it to your system PATH

## Usage

Run the script from the command line:

```
python youtube_audio_downloader.py
```

The script will prompt you for the following information:

1. YouTube video URL
2. Output filename (including extension, e.g., song.mp3)
3. Audio codec (mp3, m4a, opus, etc.)
4. Bitrate (e.g., 128, 192, 320)

After providing the required information, the script will download the audio and save it in the specified format.

## Example

```
Enter the YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Enter the output filename (with extension, e.g., song.mp3): never_gonna_give_you_up.mp3
Choose the audio codec (mp3, m4a, opus, etc.): mp3
Choose the bitrate (e.g., 128, 192, 320): 192
```

## How it works

1. The script uses `yt-dlp` to fetch the best available audio stream from the provided YouTube URL.
2. It then uses FFmpeg (via `yt-dlp`) to extract the audio and convert it to the specified format and quality.
3. The resulting audio file is saved in the same directory as the script, unless otherwise specified.

## Customization

You can modify the `download_youtube_video_as_audio` function to add more features or change default behaviors. For example, you could add options for:

- Specifying an output directory
- Downloading multiple videos at once
- Adding metadata to the audio files

## Legal Disclaimer

This script is for personal use only. Ensure you have the right to download and use the audio content as per YouTube's terms of service and applicable copyright laws.
