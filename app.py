import os
import sys
from dotenv import load_dotenv
from utility.logging import log_response
from utility.script_generator import generate_script, create_prompt
from utility.audio_generator import generate_audio
from utility.timed_captions_generator import generate_timed_captions
from utility.image_generator import generate_image_prompts, generate_images_and_videos
from utility.render_engine import get_output_media
import asyncio  # Add this import


# Load environment variables
load_dotenv()

# Function to generate content
async def generate_content(topic):
    prompt = create_prompt(topic)
    script = generate_script(prompt)
    print("Generating content", script)
    
    audio_file = "output_audio.mp3"
    await generate_audio(script, audio_file)  # Await the audio generation
    
    captions_timed = generate_timed_captions(audio_file)
    
    prompts = generate_image_prompts(script)  # Ensure this returns a valid list
    if not prompts:  # Check if prompts is empty or None
        print("No prompts generated.")
        return None, audio_file, [], []  # Return early if no prompts
    
    image_files, video_files = generate_images_and_videos(prompts)  # Updated to get video files
    
    if not image_files and not video_files:
        print("No images or videos were generated due to rate limiting or other errors.")

    output_file = get_output_media(audio_file, captions_timed, image_files, video_files)  # Pass video files

    return script, audio_file, image_files, video_files, output_file

def main(topic):
    script, audio_file, image_files, output_file = asyncio.run(generate_content(topic))  # Run the async function
    print(f"Script: {script}")
    print(f"Audio File: {audio_file}")
    print(f"Image Files: {image_files}")
    print(f"Output File: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <topic>")
        sys.exit(1)
    
    topic = sys.argv[1]
    main(topic)