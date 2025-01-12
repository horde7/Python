import os
import sys
import subprocess

def install(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_mp3(youtube_url, output_path='.'):
    """
    Download an MP3 from a YouTube video URL
    
    Args:
        youtube_url (str): URL of the YouTube video
        output_path (str, optional): Directory to save the MP3. Defaults to current directory.
    
    Returns:
        str: Path to the downloaded MP3 file
    """
    try:
        # Attempt to import libraries, install if not found
        try:
            from pytube import YouTube
        except ImportError:
            print("Installing pytube...")
            install('pytube')
            from pytube import YouTube
        
        try:
            from moviepy.editor import AudioFileClip
        except ImportError:
            print("Installing moviepy...")
            install('moviepy')
            from moviepy.editor import AudioFileClip
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Download the YouTube video
        yt = YouTube(youtube_url)
        
        # Get the highest resolution audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Download the audio file
        print(f"Downloading audio from: {yt.title}")
        downloaded_file = audio_stream.download(output_path=output_path)
        
        # Convert to MP3
        base, ext = os.path.splitext(downloaded_file)
        mp3_file = base + '.mp3'
        
        # Use moviepy to convert to MP3
        audio_clip = AudioFileClip(downloaded_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        
        # Remove the original downloaded file
        os.remove(downloaded_file)
        
        print(f"Successfully downloaded MP3: {mp3_file}")
        return mp3_file
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Example usage
    url = input("Enter the YouTube video URL: ")
    download_mp3(url)

if __name__ == "__main__":
    main()
