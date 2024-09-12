import os
import json
from datetime import datetime

LOG_TYPE_GPT = "GPT"
DIRECTORY_LOG_GPT = ".logs/gpt_logs"

def log_response(log_type, query, response):
    log_entry = {
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    directory = DIRECTORY_LOG_GPT
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{log_type.lower()}.txt'
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as outfile:
        json.dump(log_entry, outfile)