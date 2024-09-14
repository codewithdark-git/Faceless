import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from utility.logging import log_response
from utility.script_generator import generate_script
from utility.audio_generator import generate_audio
from utility.timed_captions_generator import generate_timed_captions
from utility.image_generator import generate_image_prompts, generate_images
from utility.render_engine import get_output_media

# Load environment variables
load_dotenv()

# Define async function to run in Streamlit
async def generate_content(topic):
    st.write("Generating script for topic:", topic)
    script = generate_script(topic)
    st.write("Generated Script:")
    st.write(script)

    audio_file = "output_audio.mp3"
    
    st.write("Generating audio...")
    await generate_audio(script, audio_file)
    st.write(f"Audio generated and saved to {audio_file}")

    st.write("Generating timed captions...")
    captions_timed = generate_timed_captions(audio_file)
    st.write("Timed Captions:")
    st.write(captions_timed)

    st.write("Generating images from prompts...")
    prompts = generate_image_prompts(script)
    image_files = generate_images(prompts)
    st.write("Generated Images:")
    st.image(image_files, caption=prompts, use_column_width=True)

    st.write("Rendering output media...")
    output_file = get_output_media(audio_file, captions_timed, image_files)
    st.write(f"Output media generated: {output_file}")

    # Provide a link to download the output video file
    with open(output_file, 'rb') as f:
        st.download_button(label="Download Output Video", data=f, file_name=output_file, mime='video/mp4')

# Define the Streamlit app layout
def main():
    st.title("AI Media Content Generator")
    st.write("This app generates audio, images, and captions based on a topic using AI.")

    # Input field for the topic
    topic = st.text_input("Enter a topic:", "Future of AI")

    # Run the generation when button is clicked
    if st.button("Generate Content"):
        # Run the asynchronous function using asyncio and Streamlit's `st.experimental_singleton` to handle async calls
        asyncio.run(generate_content(topic))

if __name__ == "__main__":
    main()
