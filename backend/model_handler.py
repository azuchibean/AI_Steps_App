# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HUGGING_FACE_TOKEN")


def llm_test():

    model_id = "deepset/roberta-base-squad2"

    pipe = pipeline(
        "question-answering",
        model=model_id,
        tokenizer=model_id,
    )


    
    question = "According to the context, which park is the furthest away and therefore the best to visit?"

    context = """
In Vancouver, there are several parks including Stanley Park that is 800 meters away, 
Fraserview Park that is 620 meters away, Queen Elizabeth Park that is 910 meters away

The best park to visit is the one that has the greatest distance.
"""


    response = pipe(question=question, context=context)

    return response["answer"]
