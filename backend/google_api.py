import requests
from dotenv import load_dotenv
import os

from utils.places_filter import filter_places_by_radius

load_dotenv()

API_KEY = os.getenv("GOOGLE_API")

# Central coordinate
latitude = 49.224090
longitude = -123.063501

# Radius in meters (5000 ft ≈ 1524 meters) (give it a number higher than desired for filtering)
radius = 1624

# Tolerance (how far from radius) in meters
tolerance = 100

# Actual radius because google maps only finds locations within the radius set
desired_radius = radius - 100


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Define parameters for the API request
params = {
    "location": f"{latitude},{longitude}",
    "radius": radius,
    "key": API_KEY,
    "type": "restaurant",  # test restaurants only
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Process the results
if "results" in data:
    for place in data["results"]:
        name = place.get("name")
        place_lat = place["geometry"]["location"]["lat"]
        place_lng = place["geometry"]["location"]["lng"]
        print(f"Name: {name}, Location: ({place_lat}, {place_lng})")
else:
    print("No places found or an error occurred:", data.get("error_message"))

places_within_radius = filter_places_by_radius((latitude, longitude), data, desired_radius, tolerance)

if places_within_radius:
    for name, distance in places_within_radius:
        print(f"Place near radius: {name} at {distance:.2f} m")
else:
    print("No places found within the specified radius.")
