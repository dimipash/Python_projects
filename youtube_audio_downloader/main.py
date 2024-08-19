import yt_dlp


def download_youtube_video_as_audio(
    youtube_url,
    output_path="./",
    output_filename="output.mp3",
    codec="mp3",
    bitrate="192",
):
    try:
        # Set up options for downloading
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{output_path}/{output_filename}",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": codec,
                    "preferredquality": bitrate,
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        print(f"Downloaded and converted to audio: {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    filename = input("Enter the output filename (with extension, e.g., song.mp3): ")
    codec = input("Choose the audio codec (mp3, m4a, opus, etc.): ").lower()
    bitrate = input("Choose the bitrate (e.g., 128, 192, 320): ")

    download_youtube_video_as_audio(
        url, output_filename=filename, codec=codec, bitrate=bitrate
    )
