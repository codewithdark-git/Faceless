import g4f
from g4f.client import Client
import json

def generate_script(prompt):
    client = Client()
    response = client.chat.completions.create(
        model='gpt-4',  # Replace with the correct model identifier
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    content = response.choices[0].message.content
    
    return content

def create_prompt(topic):
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 50 seconds (approximately 140 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        Weird facts
        You would produce content like this:

        Weird facts you don't know:
        - Bananas are berries, but strawberries aren't.
        - A single cloud can weigh over a million pounds.
        - There's a species of jellyfish that is biologically immortal.
        - Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.
        - The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.
        - Octopuses have three hearts and blue blood.

        You are now tasked with creating the best short script based on the user's requested type of 'facts'.

        Keep it brief, highly interesting, and unique.

        Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )
    return prompt + "\n\n" + topic


def extract_keywords(prompt):
    # Construct the API prompt to ask for keywords
    keyword_prompt = (
        """You are an expert in text analysis. I need you to extract the most relevant keywords from the following prompt.
        
        Prompt:
        {}
        
        Please provide a list of keywords separated by commas."""
    ).format(prompt)

    return keyword_prompt