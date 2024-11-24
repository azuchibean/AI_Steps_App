from geopy.distance import geodesic

def filter_places_by_radius(center, data, search_radius, tolerance=100):
    """Filter places based on distance from a central point."""
    results_within_radius = []

    for place in data["results"]:
        place_coord = (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
        distance = geodesic(center, place_coord).meters

        if distance <= search_radius + tolerance:
            
            # Ensure 'rating' key exists before accessing it
            rating = place.get('rating', None)
            if rating is not None:
                url = "https://www.google.com/maps/place/?q=place_id:"
                place_url = f'{url}{place["place_id"]}'
                results_within_radius.append((place['name'], place['vicinity'], distance, rating, place_url))

    # Sort the results by rating in descending order and retrieve the top three
    top_three_places = sorted(results_within_radius, key=lambda x: x[3], reverse=True)[:3]

    return top_three_places
