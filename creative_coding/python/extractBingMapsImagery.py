import requests
import os
import config
import pandas as pd


# map config
zoom_level = 15
map_size = "500,500"
map_style = "Aerial"
output_dir = "output/bing_imagery"


def get_bing_map_image(center_latitude, center_longitude):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "center": f"{center_latitude},{center_longitude}",
        "zoomlevel": zoom_level,
        "mapSize": map_size,
        "format": "jpeg",
        "key": config.bing_api_key,
    }

    # Create the full URL for the API request
    full_url = base_url + map_style + "/" + params["center"] + "/" + str(params["zoomlevel"]) + "?mapSize=" + params["mapSize"] + "&format=" + params["format"] + "&key=" + params["key"]

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

# Read the CSV file
df = pd.read_csv('creative_coding/data/transmitter_subset.csv')

# Loop over each row in the DataFrame
for _, row in df.iterrows():
    # Get the coordinates from the 'transmitter_site' column
    # Assuming the column contains strings like '47.6097,-122.3331'
    center_latitude, center_longitude = map(float, row['transmitter_site'].split(','))

    # Download the image for these coordinates
    get_bing_map_image(center_latitude, center_longitude)

    # Loop over each row in the DataFrame
# for i, row in df.iterrows():
#     # Get the coordinates from the 'transmitter_site' column
#     # Assuming the column contains strings like '47.6097,-122.3331'
#     center_latitude, center_longitude = map(float, row['transmitter_site'].split(','))

#     # Download the image for these coordinates
#     get_bing_map_image(center_latitude, center_longitude)

#     # Print a message
#     print(f"Downloaded image {i+1} for coordinates ({center_latitude}, {center_longitude})")


print("done.")