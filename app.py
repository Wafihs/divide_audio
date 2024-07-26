import os
import streamlit as st
from pydub import AudioSegment
from io import BytesIO

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

            num_parts=st.number_input("Enter number of parts", min_value=2, max_value=10)

            if st.button("Divide"):
                st.session_state.segments = save_audio_segments(audio, num_parts, uploaded_file.name.split('.')[0], file_format)

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
