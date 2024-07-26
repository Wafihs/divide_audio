import streamlit as st
from pydub import AudioSegment
from io import BytesIO


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
    
    AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
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
