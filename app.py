import os
import streamlit as st
import subprocess
import requests
import zipfile
from pydub import AudioSegment
from io import BytesIO

# Run setup script to install ffmpeg if it's not already installed
if not os.path.exists("/usr/bin/ffmpeg"):
    os.system("apt-get update && apt-get install -y ffmpeg")

def download_ffmpeg():
    url = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-release-essentials.zip"
    ffmpeg_dir = "ffmpeg"
    
    # Create a directory to store ffmpeg
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)
    
    ffmpeg_zip = os.path.join(ffmpeg_dir, "ffmpeg.zip")
    
    # Download ffmpeg zip file
    with requests.get(url, stream=True) as r:
        with open(ffmpeg_zip, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # Extract the zip file
    with zipfile.ZipFile(ffmpeg_zip, "r") as zip_ref:
        zip_ref.extractall(ffmpeg_dir)
    
    # Find the ffmpeg binary
    for root, dirs, files in os.walk(ffmpeg_dir):
        if "ffmpeg" in files:
            return os.path.join(root, "ffmpeg")
    return None

# Check if FFmpeg is installed
ffmpeg_path = download_ffmpeg()
if ffmpeg_path and os.path.exists(ffmpeg_path):
    st.write(f"FFmpeg is available at: {ffmpeg_path}")
    # Set the environment variable for pydub
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
else:
    st.write("Failed to install FFmpeg again.")

# Verify FFmpeg installation
ffmpeg_path = os.popen("which ffmpeg").read().strip()
if ffmpeg_path:
    st.write(f"FFmpeg is available at: {ffmpeg_path}")
else:
    st.write("FFmpeg is not installed 1.")


# Check if FFmpeg is available
try:
    ffmpeg_path = os.popen("which ffmpeg").read().strip()
    if ffmpeg_path:
        st.write(f"FFmpeg is available at: {ffmpeg_path}")
    else:
        st.write("FFmpeg is not installed 2.")
    
    # Display environment variables
    st.write("Environment Variables:")
    st.write(os.environ)
    
    # Display installed packages
    st.write("Installed Packages:")
    st.write(os.popen("pip freeze").read())
except Exception as e:
    st.write(f"An error occurred: {e}")

def save_audio_segments(audio, interval, filename_prefix, audio_format):
    segments = []
    for i in range(0, len(audio), interval):
        segment = audio[i:i + interval]
        segment_file = f"{filename_prefix}_part_{i // interval}.{audio_format}"
        segments.append((segment, segment_file))
    return segments

def main():
    st.title("Audio File Divider")

    # Initialize session state for segments if not already present
    if 'segments' not in st.session_state:
        st.session_state.segments = []

    # File upload
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "ogg", "aac", "wma", "m4a"])

    if uploaded_file is not None:
        # Determine the format of the uploaded file
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        
        file_format = uploaded_file.name.split('.')[-1]
        
        # Read audio file from uploaded file
        try:
            audio = AudioSegment.from_file(uploaded_file, format=file_format)
            
            # Get duration of the audio in seconds
            duration = len(audio) // 1000

            # Input for interval in minutes
            interval_min = st.number_input("Enter interval in minutes", min_value=1, max_value=duration // 60)
            interval_ms = interval_min * 60 * 1000

            if st.button("Divide"):
                st.session_state.segments = save_audio_segments(audio, interval_ms, uploaded_file.name.split('.')[0], file_format)

        except Exception as e:
            st.error(f"Error processing audio file: {e}")

    # Provide download links for the segments
    if st.session_state.segments:
        st.subheader("Download Segments")
        for segment, filename in st.session_state.segments:
            buffer = BytesIO()
            segment.export(buffer, format=filename.split('.')[-1])
            buffer.seek(0)
            st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime=f"audio/{filename.split('.')[-1]}")

if __name__ == "__main__":
    main()
