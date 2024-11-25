import requests
from dotenv import load_dotenv
import os

from utils.places_filter import filter_places_by_radius

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
API = os.getenv("GOOGLE_API")

def location_finder(user_latitude, user_longitude, user_height, steps_to_take, place_type):
    """
    Finds top three locations sorted according to Google Maps Rating that closely meet step count.
    """
    # Stride length formula found online
    stride_length = user_height / 100 * 0.4

    # Add 100 meters to search locations slightly further than search radius
    search_radius = stride_length * steps_to_take + 100

    params = {
        "location": f"{user_latitude},{user_longitude}",
        "radius": search_radius,
        "key": API_KEY,
        "type": place_type,
    }

    # Make the API request
    response = requests.get(API, params=params)

    # Parse the response JSON
    data = response.json()

    # Handle Places API errors
    if "error_message" in data:
        print(f"API error: {data['error_message']}")
        return
    
    # Handles empty response from Places API
    if data["status"] == "ZERO_RESULTS":
        print("No results for places at chosen location and step count.")
        return

    # Process the results
    places_within_radius = filter_places_by_radius(
        (user_latitude, user_longitude), data, search_radius
    )

    places_json_list = []

    if places_within_radius:
        for name, address, distance, rating, url in places_within_radius:
            place_data = {
                "name": name,
                "address": address,
                "distance": round(distance, 2),
                "rating": rating,
                "url": url
            }
            places_json_list.append(place_data)
    else:
        return {"response": "No places found within the specified radius."}

    return places_json_list
