from diffusers import DiffusionPipeline
import torch
import re
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()

# Ensure GPU is used if available
device = "cuda" if torch.cuda.is_available() else "cpu"
from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("Shakker-Labs/AWPortrait-FL")

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
        image = pipeline(prompt).images[0]
        filename = f"generated_image_{idx}.png"
        image.save(filename)
        image_files.append(filename)
    
    return image_files