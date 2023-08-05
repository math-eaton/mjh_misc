import pandas as pd
import requests
import os
import io
import config
from PIL import Image
from process_imagery import process_image


# map config
map_size = "500,500"
map_style = "Aerial"
output_dir = "output/bing_imagery/area"


def get_bing_map_image(min_latitude, min_longitude, max_latitude, max_longitude, application_id):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "mapArea": f"{min_latitude},{min_longitude},{max_latitude},{max_longitude}",
        "mapSize": map_size,
        "format": "png",
        "key": config.bing_api_key,
    }

    # Create the full URL for the API request
    full_url = base_url + map_style + "?" + "&".join(f"{key}={value}" for key, value in params.items())

    # Make the API request
    response = requests.get(full_url)

    # Check that the request was successful
    if response.status_code == 200:

        # Open the image using PIL
        image = Image.open(io.BytesIO(response.content))

        # Define the dimensions for the crop
        crop_percentage = 20  # percentage to crop from the bottom
        crop_pixel = int((crop_percentage/100) * image.height)  # calculate the number of pixels to crop

        left = 0
        top = 0
        right = image.width
        bottom = image.height - crop_pixel  # subtract the crop pixels from the height

        # Adjust left and right to maintain square aspect ratio
        square_size = min(right, bottom)  # size of the square is the smaller of width and height
        left = (image.width - square_size) / 2
        right = left + square_size

        # Crop the image
        image = image.crop((left, top, right, bottom))

        # Define the output file path
        output_file_path = os.path.join(output_dir, f"{application_id}.png")

        # Save the image
        image.save(output_file_path)
        
        # Process the image
        processed_output_path = os.path.join("output/bing_imagery/area", f"{application_id}.png")
        process_image(output_file_path, processed_output_path)

    else:
        print(f"Failed to get map image: {response.content}")

# Read the CSV file and get the first 10 rows for debugging purposes
df = pd.read_csv('creative_coding/data/fm_contours_sample.csv').head(10)

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
    get_bing_map_image(min_latitude, min_longitude, max_latitude, max_longitude, row['application_id'])

print("done.")
