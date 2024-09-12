from diffusers import DiffusionPipeline
import torch
import re
from PIL import Image
import io

def generate_image_prompts(script):
    # Split the script into sentences
    sentences = re.split(r'(?<=[.!?]) +', script)
    
    # Generate prompts for each sentence
    prompts = []
    for sentence in sentences:
        if sentence.strip():  # Ensure the sentence is not empty
            prompts.append(sentence.strip())
    
    return prompts

def generate_images(prompts):

    pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")
    pipe = pipe.to(device)

    image_files = []
    for idx, prompt in enumerate(prompts):
        print(f"Generating image for prompt: {prompt}")
        image = pipe(prompt).images[0]
        filename = f"generated_image_{idx}.png"
        image.save(filename)
        image_files.append(filename)
    
    return image_files