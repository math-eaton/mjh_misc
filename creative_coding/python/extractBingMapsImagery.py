import requests
import os
import config

# map config
zoom_level = 4
map_size = "500,500"
map_style = "Aerial"
output_dir = "/Users/matthewheaton/Documents/GitHub/mjh_misc/output/bing_imagery"


def get_bing_map_image(center_latitude, center_longitude):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "mapArea": f"{center_latitude-0.01},{center_longitude-0.01},{center_latitude+0.01},{center_longitude+0.01}",
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
        # Define the output file path
        output_file_path = os.path.join(output_dir, f"map_{center_latitude}_{center_longitude}.jpg")

        # Save the image
        with open(output_file_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to get map image: {response.content}")

# Example usage
get_bing_map_image(47.6097, -122.3331)
