from transformers import pipeline
import json

def generate_script(topic):
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

    generator = pipeline('text-generation', model='mistralai/Mistral-Nemo-Instruct-2407')
    response = generator(prompt + "\n\n" + topic, max_length=200, num_return_sequences=1)
    
    content = response[0]['generated_text']
    try:
        script = json.loads(content)["script"]
    except json.JSONDecodeError:
        print("JSONDecodeError. Attempting to extract JSON from the response.")
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        script = json.loads(content[json_start:json_end])["script"]
    
    return script