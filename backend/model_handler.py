# destination_finder.py
from transformers import AutoTokenizer, AutoModel
import torch

# Load DistilBERT tokenizer and model
model_name = "distilbert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Hardcoded example destinations in Vancouver
example_destinations = [
    {"name": "Stanley Park", "address": "Vancouver, BC V6G 1Z4, Canada"},
    {"name": "Granville Island", "address": "1669 Johnston St, Vancouver, BC V6H 3R9, Canada"},
    {"name": "Grouse Mountain", "address": "6400 Nancy Greene Way, North Vancouver, BC V7R 4K9, Canada"},
    {"name": "Capilano Suspension Bridge", "address": "3735 Capilano Rd, North Vancouver, BC V7R 4J8, Canada"},
    {"name": "Gastown", "address": "Water St, Vancouver, BC V6B 1A1, Canada"},
    {"name": "Vancouver Aquarium", "address": "845 Avison Way, Vancouver, BC V6G 3E2, Canada"},
    {"name": "Science World", "address": "1455 Quebec St, Vancouver, BC V6A 3Z7, Canada"},
    {"name": "Queen Elizabeth Park", "address": "4600 Cambie St, Vancouver, BC V5Z 2Z1, Canada"},
    {"name": "Lynn Canyon Park", "address": "3663 Park Rd, North Vancouver, BC V7J 3K6, Canada"},
    {"name": "Pacific Centre", "address": "701 W Georgia St, Vancouver, BC V7Y 1G5, Canada"}
]

def process_input(user_input: str):
    # Tokenize input text
    inputs = tokenizer(user_input, return_tensors="pt")

    # Forward pass to get the embeddings (not used for filtering in this example)
    with torch.no_grad():
        outputs = model(**inputs)

    # Return the processed input (not used further in this example)
    return user_input

def get_top_destinations(user_query: str, destinations, top_n=3):
    # Define keywords for filtering based on the user's query
    keywords = []
    
    if "park" in user_query.lower():
        keywords.append("park")
    if "restaurant" in user_query.lower():
        keywords.append("restaurant")
    
    # Filter destinations based on keywords
    filtered_destinations = []
    
    for destination in destinations:
        if any(keyword in destination["name"].lower() for keyword in keywords):
            filtered_destinations.append(destination)

    # Return only the top N destinations
    return filtered_destinations[:top_n]

def find_top_destinations(user_query: str, top_n=3):
    # Process the input (e.g., extracting keywords, etc.)
    processed_query = process_input(user_query)

    # Get the top destinations based on user query
    top_destinations = get_top_destinations(processed_query, example_destinations, top_n)

    return top_destinations
