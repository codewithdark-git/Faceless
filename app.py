import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from utility.logging import log_response
from utility.script_generator import generate_script
from utility.audio_generator import generate_audio
from utility.timed_captions_generator import generate_timed_captions
from utility.image_generator import generate_image_prompts, generate_images
from utility.render_engine import get_output_media

load_dotenv()

SAMPLE_TOPIC = "Future OF AI"
SAMPLE_FILE_NAME = "sample_audio.mp3"

async def main():
    topic = SAMPLE_TOPIC
    script = generate_script(topic)
    print("Script:", script)
    audio_file = SAMPLE_FILE_NAME
    await generate_audio(script, audio_file)
    captions_timed = generate_timed_captions(audio_file)
    print("Timed Captions:", captions_timed)
    prompts = generate_image_prompts(script)
    image_files = generate_images(prompts)
    output_file = get_output_media(audio_file, captions_timed, image_files)
    print("Output video file:", output_file)

if __name__ == "__main__":
    asyncio.run(main())