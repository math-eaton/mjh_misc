import pandas as pd
import requests
import os
import config

# map config
map_size = "500,500"
map_style = "Aerial"
output_dir = "output/bing_imagery/area"

def get_bing_map_image(min_latitude, min_longitude, max_latitude, max_longitude, row_index):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "mapArea": f"{min_latitude},{min_longitude},{max_latitude},{max_longitude}",
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
        output_file_path = os.path.join(output_dir, f"map_{row_index}_{min_latitude}_{min_longitude}_{max_latitude}_{max_longitude}.jpg")

        # Save the image
        with open(output_file_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to get map image: {response.content}")

# Read the CSV file
df = pd.read_csv('creative_coding/data/fm_contours_sample.csv')

# Loop over each row in the DataFrame
for index, row in df.iterrows():
    # Initialize min and max coordinates for each row
    min_latitude = 90
    max_latitude = -90
    min_longitude = 180
    max_longitude = -180

    # Loop over each column in the row
    for i in range(360):
        # Check if the column value is a valid latitude/longitude pair
        if ',' in row[str(i)]:
            try:
                # Get the coordinates from the column
                latitude, longitude = map(float, row[str(i)].split(','))

                # Update min and max coordinates
                min_latitude = min(min_latitude, latitude)
                max_latitude = max(max_latitude, latitude)
                min_longitude = min(min_longitude, longitude)
                max_longitude = max(max_longitude, longitude)
            except ValueError:
                # Ignore the column if it's not a valid latitude/longitude pair
                pass

    # Download the image for these coordinates
    get_bing_map_image(min_latitude, min_longitude, max_latitude, max_longitude, index)

print("done.")
