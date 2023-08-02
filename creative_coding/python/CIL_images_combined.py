import requests
from PIL import Image
from io import BytesIO
import os
import random
import time
import numpy as np

# Define the number of images to download
num_images = 5

# Define the output folder
output_folder = "/Users/matthewheaton/Documents/CIL_API_output"

# Base URL for the API
api_url = "https://cilia.crbs.ucsd.edu/rest"

# Authentication details
username = 'columbia_edu'
password = 'nkWBqPTAHGDdlz0'

# Define the fields for CCDB images
ccdb_fields = [
    "CIL_CCDB.CCDB.Recon_Display_image.URL",
    "CIL_CCDB.CCDB.Image2d.Image2D_Display_image.URL",
    "CIL_CCDB.CCDB.Segmentation.Seg_Display_image.URL",
]

# Function to crop an image
def crop_image(image, sensitivity=0):
    # Convert the image to a NumPy array
    image_data = np.array(image)

    if len(image_data.shape) == 3:  # RGB Image
        # Identify non-mono pixels
        non_white_black = np.any(image_data < (255 - sensitivity), axis=-1) & np.any(image_data > sensitivity, axis=-1)
    else:  # Grayscale Image
        non_white_black = (image_data < (255 - sensitivity)) & (image_data > sensitivity)

    # Get the bounding box of the non-mono pixels
    non_white_black_bounding_box = np.argwhere(non_white_black)

    # Crop the image to the bounding box
    cropped_image = image_data[non_white_black_bounding_box.min(axis=0)[0]:non_white_black_bounding_box.max(axis=0)[0] + 1,
                               non_white_black_bounding_box.min(axis=0)[1]:non_white_black_bounding_box.max(axis=0)[1] + 1]

    # Return the cropped image
    return Image.fromarray(cropped_image)

# Function to process an image
def process_image(image):
    # Resize the image (pre-dither) using nearest neighbor
    size = (400, 400)  # Set your desired size here
    image = image.resize(size, Image.NEAREST)
    print("Resizing...")

    # Convert the image to grayscale
    image = image.convert('L')

    # Dither the image
    image = image.convert('1')
    print("Dithering...")

    # Convert the image back to RGB
    image = image.convert('RGB')

    # Make sure the image has an alpha channel
    image = image.convert('RGBA')

    # Convert white (also shades of whites) pixels to transparent
    data = np.array(image)
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    white_areas = (red > 200) & (green > 200) & (blue > 200)
    data[white_areas] = [255, 255, 255, 0]
    image = Image.fromarray(data)

    # Resize the image (post-dither) using nearest neighbor
    size = (300, 300)  # Set your desired size here
    image = image.resize(size, Image.NEAREST)

    return image

# Function to get a random image from the API
def download_image(image_id):
    try:
        # Fetch the document data from the API
        response = requests.get(f"{api_url}/public_documents/{image_id}", auth=(username, password), timeout=5)
        response.raise_for_status()
        data = response.json()

        # Check the ID type
        if image_id.startswith("CCDB_"):
            # Check each field
            for field in ccdb_fields:
                # Get the image URL from the API response
                image_url = data.get(field)
                if image_url:
                    # Fetch the image data
                    response = requests.get(image_url, stream=True, timeout=5)
                    response.raise_for_status()

                    # Load the image data with PIL
                    image = Image.open(BytesIO(response.content))

                    # Crop the image
                    image = crop_image(image)

                    # Process the image
                    image = process_image(image)

                    # Save the image
                    filename = os.path.join(output_folder, f"{image_id}.png")
                    image.save(filename, "PNG")
        elif image_id.startswith("CIL_"):
            # Remove the "CIL_" prefix
            id_number = image_id[4:]

            # Construct the image URL
            image_url = f"https://cildata.crbs.ucsd.edu/media/thumbnail_display/{id_number}/{id_number}_thumbnailx512.jpg"

            # Fetch the image data
            response = requests.get(image_url, stream=True, timeout=5)
            response.raise_for_status()

            # Load the image data with PIL
            image = Image.open(BytesIO(response.content))

            # Crop the image
            image = crop_image(image)

            # Process the image
            image = process_image(image)

            # Save the image
            filename = os.path.join(output_folder, f"{image_id}_{image.size[0]}x{image.size[1]}.png")
            image.save(filename, "PNG")


    except requests.exceptions.Timeout:
        print(f"Request timed out for image ID: {image_id}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Image not found for ID: {image_id}")
        else:
            print(f"HTTP error occurred for image ID: {image_id}. Error details: {str(e)}")
    except Exception as e:
        print(f"An error occurred for image ID: {image_id}. Error details: {str(e)}")

# Fetch the list of public IDs
response = requests.get(f"{api_url}/public_ids?from=0&size=50000", auth=(username, password))
response.raise_for_status()

# Get the list of IDs
ids = [hit['_id'] for hit in response.json()['hits']['hits']]

# Randomly shuffle the list of IDs
# with new seed for random based on current time
random.seed(time.time())
random.shuffle(ids)

# Download the images
for i in range(min(num_images, len(ids))):
    download_image(ids[i])
    print(f"Downloading... ({i+1} of {min(num_images, len(ids))})")

print("Done.")