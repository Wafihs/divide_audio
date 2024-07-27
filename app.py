import os
import tempfile
import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import time

##Work
def save_audio_segments(audio, num_parts, filename_prefix, audio_format):
    segments = []
    part_duration = len(audio) // num_parts
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration if i != num_parts - 1 else len(audio)
        segment = audio[start_time:end_time]
        segment_file = f"{filename_prefix}_part_{i + 1}.{audio_format}"
        segments.append((segment, segment_file))
        time.sleep(10)
        st.write("Inside loop")
        check4=st.number_input("Continue 4?")
    return segments

def main():
    st.title("Audio File Divider")

    # Initialize session state for segments if not already present
    if 'segments' not in st.session_state:
        st.session_state.segments = []
    if 'num_parts' not in st.session_state:
        st.session_state.num_parts = 2
    if 'audio' not in st.session_state:
        st.session_state.audio = None
    if 'file_format' not in st.session_state:
        st.session_state.file_format = None
    if 'file_name' not in st.session_state:
        st.session_state.file_name = ""
    if 'duration' not in st.session_state:
        st.session_state.duration = None

    # File upload
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "ogg", "aac", "wma", "m4a"])

    if uploaded_file is not None:
        # Determine the format of the uploaded file
        st.session_state.filename = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        file_format = uploaded_file.name.split('.')[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_format}") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Read audio file from uploaded file
        try:
            st.session_state.audio = AudioSegment.from_file(temp_file_path, format=file_format)
            st.session_state.file_format = file_format
            check1=st.number_input("Continue 1?")

        except Exception as e:
            st.error(f"Error processing audio file: {e} Error type: {type(e).__name__}")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        # Get duration of the audio in seconds
        st.session_state.duration = len(st.session_state.audio) // 1000

        num_parts_input=st.number_input("Enter number of parts", min_value=2, max_value=10, value=st.session_state.num_parts)

        if st.button("Set Number of Parts"):
          st. session_state.num_parts = num_parts_input
              
    if st.button("Divide") and st.session_state.audio:
      check3=st.number_input("Continue 3?")
      st.session_state.segments = save_audio_segments(st.session_state.audio, st.session_state.num_parts, st.session_state.filename.split('.')[0], st.session_state.file_format)
      os.remove(temp_file_path)

    # Provide download links for the segments
    if st.session_state.segments:
        st.subheader("Download Segments")
        for segment, filename in st.session_state.segments:
            buffer = BytesIO()
            segment.export(buffer, format=filename.split('.')[-1])
            buffer.seek(0)
            st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime=f"audio/{filename.split('.')[-1]}")

# Add footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: var(--primary-background-color);
            color: var(--primary-color);
            text-align: center;
        }
        </style>
        <div class="footer">
            <p>Made by Wafi</p>
        </div>
        """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
