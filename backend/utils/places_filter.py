from geopy.distance import geodesic

# Uses geopy to filter for locations in a certain range
def filter_places_by_radius(center, data, desired_radius, tolerance):
    """Filter places based on distance from a central point."""
    results_within_radius = []

    for place in data["results"]:
        place_coord = (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
        distance = geodesic(center, place_coord).meters

        if abs(distance - desired_radius) <= tolerance:
            results_within_radius.append((place['name'], distance))

    return results_within_radius
