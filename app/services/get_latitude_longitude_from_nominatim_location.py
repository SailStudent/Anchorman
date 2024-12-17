import requests

def get_latitude_longitude_from_nominatim_location(location_name):
    try:
        response = requests.get(
            url="https://osm-nominatim.gs.mil/search",
            params={"q": location_name, "format": "jsonv2"}, timeout=90
        )
        response.raise_for_status()
        json_response = response.json()
        if not json_response:
            raise ValueError("Empty response")
        location_data = json_response[0]
        latitude, longitude = round(float(location_data['lat']), 2), round(float(location_data['lon']), 2)
        return latitude, longitude
    except Exception as e:
        print(f"Error getting nominatim.gs.mil coordinates for {location_name}: {e}")
        return None
get_latitude_longitude_from_nominatim_location("Detroit")  # (42.33, -83.05)