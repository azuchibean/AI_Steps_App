import requests
from dotenv import load_dotenv
import os

from utils.places_filter import filter_places_by_radius

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
API = os.getenv("GOOGLE_API")

# Supported types: https://developers.google.com/maps/documentation/places/web-service/supported_types
def location_finder(latitude, longitude, height, steps, type):
    try:
        # Calculate stride length and use to find distance
        stride_length = height/100 * 0.4
        radius = stride_length * steps

        # Actual radius because google maps only finds locations within the radius set
        desired_radius = radius - 100

        # Define parameters for the API request
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": API_KEY,
            "type": type,  # e.g., restaurant, park, bus_station, etc.
        }

        # Make the API request
        response = requests.get(API, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the response JSON
        data = response.json()

        # Handle Google API errors
        if "error_message" in data:
            print(f"API error: {data['error_message']}")
            return

        # Process the results
        places_within_radius = filter_places_by_radius(
            (latitude, longitude), data, desired_radius
        )

        places_json_list = []

        if places_within_radius:
            for name, vicinity, distance, rating in places_within_radius:
                place_data = {
                    "name": name,
                    "vicinity": vicinity,
                    "distance": round(distance, 2),
                    "rating": rating
                }
                places_json_list.append(place_data)
        else:
            return {"response":"No places found within the specified radius."}

        return places_json_list

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
