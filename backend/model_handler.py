# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
import os
from dotenv import load_dotenv
from location_finder import location_finder

load_dotenv()
hf_token = os.getenv("HUGGING_FACE_TOKEN")

def llm_run(latitude, longitude, height, steps, location_type):

    api_results = location_finder(latitude, longitude, height, steps, location_type)

    model_id = "deepset/roberta-base-squad2"

    pipe = pipeline(
        "question-answering",
        model=model_id,
        tokenizer=model_id,
    )

    
    question = f"According to the context, which {location_type} is the furthest away and therefore the best to visit?"

    context = f"In Vancouver, there are several {location_type} including:\n"
    
    # Add each park and its distance to the context
    for place in api_results:
        context += f"{place['name']} that is {place['distance']} meters away,\n"
    
    context += f"The best {location_type} to visit is the one that has the greatest distance."

    print(context)

    response = pipe(question=question, context=context)

    return response["answer"]
