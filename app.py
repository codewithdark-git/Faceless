import os
import sys
from dotenv import load_dotenv
from utility.logging import log_response
from utility.script_generator import generate_script
from utility.audio_generator import generate_audio
from utility.timed_captions_generator import generate_timed_captions
from utility.image_generator import generate_image_prompts, generate_images
from utility.render_engine import get_output_media

# Load environment variables
load_dotenv()

# Function to generate content
def generate_content(topic):
    script = generate_script(topic)
    
    audio_file = "output_audio.mp3"
    generate_audio(script, audio_file)
    
    captions_timed = generate_timed_captions(audio_file)
    
    prompts = generate_image_prompts(script)
    image_files = generate_images(prompts)
    
    if not image_files:
        print("No images were generated due to rate limiting or other errors.")
       
    output_file = get_output_media(audio_file, captions_timed, image_files)

    return script, audio_file, image_files, output_file

def main(topic):
    script, audio_file, image_files, output_file = generate_content(topic)
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