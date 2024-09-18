import time
import re
from dotenv import load_dotenv
import os
import requests
import random
from utility.script_generator import generate_script, extract_keywords

# Load environment variables
load_dotenv()

# Get Pexels API key from environment variable
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
headers = {
    'Authorization': f'Bearer {PEXELS_API_KEY}'
}

# Function to fetch an image URL from Pexels API based on a prompt
def fetch_image_from_pexels_website(prompt):
    try:
        response = requests.get(f"https://api.pexels.com/v1/search?query={prompt}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:  # Ensure there are photos in the response
                return data['photos'][0]['src']['original']  # Access the original URL of the image
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            return fetch_image_from_pexels_website(prompt)  # Retry the request
    except requests.exceptions.RequestException as e:
        print(f'Error processing request for image: {e}')
    return None

# Function to fetch a video URL from Pexels API based on a prompt
def fetch_video_from_pexels_website(prompt):
    try:
        response = requests.get(f"https://api.pexels.com/videos/search?query={prompt}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['videos']:  # Ensure there are videos in the response
                return data['videos'][0]['video_files'][0]['link']  # Access the video download link
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            return fetch_video_from_pexels_website(prompt)  # Retry the request
    except requests.exceptions.RequestException as e:
        print(f'Error processing request for video: {e}')
    return None

# Function to download a file (image or video) from a URL
def download_file(url, filename):
    if not url:
        print(f"Cannot download file. Invalid URL: {url}")  # Log invalid URL
        return
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(filename, 'wb') as f:
            f.write(response.content)  # Save content to file
        print(f"File downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")  # Log download error

# Function to generate prompts from a script
def generate_image_prompts(script):
    # Split the script into sentences
    sentences = re.split(r'(?<=[.!?]) +', script)
    
    # Generate prompts for each sentence using LLM for main keyword extraction
    keywords = []
    for sentence in sentences:
        if sentence.strip():  # Ensure the sentence is not empty
            # Extract the main keyword for the sentence using an LLM function
            sentence = extract_keywords(sentence)
            keyword = generate_script(sentence)
            keywords.append(keyword)

    return keywords

# Function to generate and download images or videos based on prompts
def generate_images_and_videos(prompts):
    image_files = []
    video_files = []  # Store video file paths
    for idx, prompt in enumerate(prompts):
        if len(image_files) >= 7 and len(video_files) >= 7:  # Limit to a maximum of 7 images and 7 videos
            break
        
        # Randomly choose to fetch either an image or a video
        if random.choice(['image', 'video']) == 'image':
            print(f"Fetching image for prompt: {prompt}")
            image_url = fetch_image_from_pexels_website(prompt)  # Fetch image URL
            if image_url:
                image_filename = f'generated_image_{idx}.png'  # Define filename for image
                download_file(image_url, image_filename)  # Download the image
                image_files.append(image_filename)
        else:
            print(f"Fetching video for prompt: {prompt}")
            video_url = fetch_video_from_pexels_website(prompt)  # Fetch video URL
            if video_url:
                video_filename = f'generated_video_{idx}.mp4'  # Define filename for video
                download_file(video_url, video_filename)  # Download the video
                video_files.append(video_filename)

    return image_files[:7], video_files[:7]