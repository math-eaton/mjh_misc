import requests
import os
import io
import config
import pandas as pd
from PIL import Image
from process_imagery import process_image

# map config
zoom_level = 15
map_size = "500,500"
map_style = "Aerial"
unprocessed_output_dir = "output/bing_imagery/point"
processed_output_dir = "output/processed_imagery/point"


def get_bing_map_image(center_latitude, center_longitude, application_id):
    # Define the base URL for the Bing Maps Static API
    base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/"

    # Define the parameters for the API request
    params = {
        "center": f"{center_latitude},{center_longitude}",
        "zoomlevel": zoom_level,
        "mapSize": map_size,
        "format": "png",
        "key": config.bing_api_key,
    }

    # Create the full URL for the API request
    full_url = base_url + map_style + "/" + params["center"] + "/" + str(params["zoomlevel"]) + "?mapSize=" + params["mapSize"] + "&format=" + params["format"] + "&key=" + params["key"]

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

        # Define the output file path for the unprocessed image
        unprocessed_output_file_path = os.path.join(unprocessed_output_dir, f"{application_id}.png")

        # Save the unprocessed image
        image.save(unprocessed_output_file_path)

        # Define the output file path for the processed image
        processed_output_file_path = os.path.join(processed_output_dir, f"{application_id}.png")

        # Process the image
        processed_image = process_image(unprocessed_output_file_path, processed_output_file_path)

        # If the image was processed successfully, save it
        if processed_image is not None:
            # Save the processed image
            processed_image.save(processed_output_file_path)
        else:
            print(f"Image for application_id {application_id} was not processed due to low resolution.")

    else:
        print(f"Failed to get map image: {response.content}")

# Read the CSV file and get the first 10 rows for debugging purposes
df = pd.read_csv('creative_coding/data/fm_contours_sample.csv').head(10)

# Loop over each row in the DataFrame
for _, row in df.iterrows():
    # Get the coordinates from the 'transmitter_site' column
    # Assuming the column contains strings like '47.6097,-122.3331'
    center_latitude, center_longitude = map(float, row['transmitter_site'].split(','))

    # Download the image for these coordinates
    get_bing_map_image(center_latitude, center_longitude, row['application_id'])

print("done.")