from diffusers import StableDiffusionPipeline
import torch
import re
from PIL import Image
import io
from dotenv import load_dotenv
import os
from together import Together
import base64

load_dotenv()


# pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
# pipe.to("cpu")
client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

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
        if len(image_files) >= 7:  # Limit to a maximum of 7 images
            break
        print(f"Generating image for prompt: {prompt}")
        # Ensure the prompt is processed on the correct device
        response = client.images.generate(
            prompt=prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
            width=1024,
            height=1024,
            steps=40,
            n=4,    
            seed=3919
        )
        image_data = response.data[0].b64_json
        filename = f'generated_image_{idx}.png'  # Define filename
        with open(filename, 'wb') as f:  # Use filename here
            f.write(base64.b64decode(image_data))
        # Load the image to save it
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))  # Create image from data
        image.save(filename)  # Save the image
        image_files.append(filename)
    
    return image_files[:7]