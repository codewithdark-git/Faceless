import gradio as gr
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

# Async function to generate content
async def generate_content_gradio(topic):
    script = generate_script(topic)
    
    audio_file = "output_audio.mp3"
    await generate_audio(script, audio_file)
    
    captions_timed = generate_timed_captions(audio_file)
    
    prompts = generate_image_prompts(script)
    image_files = generate_images(prompts)
    
    output_file = get_output_media(audio_file, captions_timed, image_files)

    return script, audio_file, image_files, output_file

# Gradio interface function
async def generate_content_interface(topic):
    script, audio_file, image_files, output_file = await generate_content_gradio(topic)
    
    # For Gradio outputs: Text for script, audio file, image(s), and output media file
    return script, audio_file, image_files, output_file

# Define Gradio app layout
def main():
    # Gradio Interface
    with gr.Blocks() as demo:
        gr.Markdown("# AI Media Content Generator")
        gr.Markdown("This app generates audio, images, and captions based on a topic using AI.")

        # Input field for the topic
        topic_input = gr.Textbox(label="Enter a topic", placeholder="Future of AI")
        
        # Outputs: Script (Text), Audio (Audio), Images (Image List), Final Media (Video)
        script_output = gr.Textbox(label="Generated Script")
        audio_output = gr.Audio(label="Generated Audio")
        images_output = gr.Gallery(label="Generated Images")
        output_media = gr.Video(label="Output Media")

        # Define the event when clicking the button
        generate_btn = gr.Button("Generate Content")
        generate_btn.click(fn=generate_content_interface, inputs=topic_input, outputs=[script_output, audio_output, images_output, output_media])

    return demo

if __name__ == "__main__":
    main().launch()
