import streamlit as st
import os
import video_processing
import ppt_generator

def main():
    st.title("Video to PowerPoint Generator")

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)

        if st.button("Generate PowerPoint"):
            with st.spinner("Generating PowerPoint..."):
                # Save uploaded file
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                video_path = os.path.join("uploads", uploaded_file.name)
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Process video
                image_paths = video_processing.extract_key_frames(video_path)

                # Generate PPT
                if image_paths:
                    texts = [f"This is slide {i+1}" for i in range(len(image_paths))]
                    ppt_generator.create_ppt(image_paths, texts)
                    st.success("PowerPoint presentation generated!")
                    
                    with open("generated/presentation.pptx", "rb") as f:
                        st.download_button(
                            label="Download PowerPoint",
                            data=f,
                            file_name="presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        )
                else:
                    st.error("No scenes detected in the video.")

if __name__ == "__main__":
    main()
