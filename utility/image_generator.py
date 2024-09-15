from diffusers import StableDiffusionPipeline
import torch
import re
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()


pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
pipe.to("cpu")

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
    image_files = []
    for idx, prompt in enumerate(prompts):
        print(f"Generating image for prompt: {prompt}")
        # Ensure the prompt is processed on the correct device
        image = pipe(prompt).images[0]
        filename = f"generated_image_{idx}.png"
        image.save(filename)
        image_files.append(filename)
    
    return image_files