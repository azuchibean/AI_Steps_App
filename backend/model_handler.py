# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
from dotenv import load_dotenv
from location_finder import location_finder

load_dotenv()

def llm_run(latitude, longitude, height, steps, location_type):
    """
    Runs Places API and uses HuggingFace LLM to recommend one of the options.
    """

    # Calls function to retrieve array of places in a range
    api_results = location_finder(latitude, longitude, height, steps, location_type)

    if not api_results:
        raise ValueError(
            "No results found from location_finder. Please check the inputs."
        )

    # LLM model
    model_id = "deepset/roberta-base-squad2"

    # Defines pipeline for LLM
    pipe = pipeline(
        "question-answering",
        model=model_id,
        tokenizer=model_id,
    )

    # Question and context for LLM to process
    question = f'Which location is the best option? The highest-rated {location_type} among the following options should be selected.'

    context = f"There are several {location_type} including:\n"

    for place in api_results:
        context += f"- {place['name']} with a rating of {place['rating']} and is {place['distance']} metres away. \n"

    context += f"The best {location_type} to visit has a large rating."

    # Send response to LLM for processing
    llm_response = pipe(question=question, context=context)

    # Package API response as json
    response = {
        "api_response" : api_results,
        "llm_recommendation" : llm_response["answer"]
    }

    return response
