import requests
from PIL import Image
from io import BytesIO
import os
import random

# Define the number of images to download
num_images = 5

# Define the output folder
output_folder = "/Users/matthewheaton/Documents/CIL_API_output"

# Define the image size (5.5 inches x 300 dpi)
image_size = (int(5.5 * 300), int(5.5 * 300))

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

# Function to get a random image from the API
def get_random_image(image_id):
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

                    # Resize the image
                    image = image.resize(image_size, Image.LANCZOS)

                    return image
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

            # Resize the image
            image = image.resize(image_size, Image.LANCZOS)

            return image

    except requests.exceptions.Timeout:
        print(f"Request timed out for image ID: {image_id}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Image not found for ID: {image_id}")
        else:
            print(f"HTTP error occurred for image ID: {image_id}. Error details: {str(e)}")
    except Exception as e:
        print(f"An error occurred for image ID: {image_id}. Error details: {str(e)}")

    return None

# Fetch the list of public IDs
response = requests.get(f"{api_url}/public_ids?from=0&size=100", auth=(username, password))
response.raise_for_status()

# Get the list of IDs
ids = [hit['_id'] for hit in response.json()['hits']['hits']]

# Randomly shuffle the list of IDs
random.shuffle(ids)

# Get and save the images
for i in range(min(num_images, len(ids))):
    # Get a random image
    image = get_random_image(ids[i])

    if image is not None:
        # Save the image
        filename = os.path.join(output_folder, f"image_{ids[i]}.png")
        image.save(filename, "PNG")
