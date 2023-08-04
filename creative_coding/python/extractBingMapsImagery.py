import requests
import os
import creative_coding.python.config as config

# map config
zoom_level = 4
map_size = "500,500"
map_style = "Aerial"
output_dir = 


def get_bing_map_image(center_latitude, center_longitude, zoom_level, map_size, map_style):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "mapArea": f"{center_latitude-0.01},{center_longitude-0.01},{center_latitude+0.01},{center_longitude+0.01}",
        "zoomLevel": zoom_level,
        "mapSize": map_size,
        "format": "jpeg",
        "key": config.bing_api_key,
    }

    # Create the full URL for the API request
    full_url = base_url + map_style + "?" + "&".join(f"{key}={value}" for key, value in params.items())

    # Make the API request
    response = requests.get(full_url)

    # Check that the request was successful
    if response.status_code == 200:
        # Save the image
        with open(f"map_{center_latitude}_{center_longitude}.jpg", "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to get map image: {response.content}")

# Example usage
get_bing_map_image(47.6097, -122.3331, 15, "500,500", "Road")
get_bing_map_image(40.7128, -74.0060, 12, "400,400", "Aerial")
