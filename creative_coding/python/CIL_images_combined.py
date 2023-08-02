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

                    # Save the image
                    filename = os.path.join(output_folder, f"{image_id}.jpg")
                    image.save(filename, "JPEG")
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

            # Save the image
            filename = os.path.join(output_folder, f"{image_id}.jpg")
            image.save(filename, "JPEG")

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

print("Download complete.")

# Define the image size (5.5 inches x 300 dpi)
image_size = (int(5.5 * 300), int(5.5 * 300))

# Define the input folder
input_folder = "/Users/matthewheaton/Documents/CIL_API_output"

# Function to resize an image
def resize_image(filename):
    # Check if the image has already been processed
    if "_resized" not in filename:
        try:
            # Load the image
            image = Image.open(filename)
            print("Loading " + filename)

            # Resize the image
            image = image.resize(image_size, Image.LANCZOS)
            print("Resizing...")

            # Save the image with a new filename
            new_filename = os.path.splitext(filename)[0] + "_resized.png"
            image.save(new_filename, "PNG")
            print("Saving...")

            # If new file is saved successfully, remove the original file
            if os.path.isfile(new_filename):
                os.remove(filename)
                print(f"Removed original file: {filename}")

        except Exception as e:
            print(f"An error occurred for file: {filename}. Error details: {str(e)}")

# Resize all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg"):
        resize_image(os.path.join(input_folder, filename))

print("Resize complete.")

# Define the directory with the images
input_folder = "/Users/matthewheaton/Documents/CIL_API_output"

# Function to process an image
def process_image(filename):
    # Define the post-processing image size
    post_size = (300, 300)  # Set your desired size here

    # Check if the image has already been processed
    if f"_{post_size[0]}x{post_size[1]}" not in filename:
        try:
            # Load the image
            image = Image.open(filename)
            print("Loading " + filename + "...")

            # Convert the image to grayscale
            grayscale_image = image.convert('L')

            # Convert the grayscale image to a numpy array
            grayscale_array = np.array(grayscale_image)

            # Find the bounding box of non-black pixels (tolerance: 10)
            rows = np.any(grayscale_array > 10, axis=1)
            cols = np.any(grayscale_array > 10, axis=0)
            rmin, rmax = np.where(rows)[0][[0, -1]]
            cmin, cmax = np.where(cols)[0][[0, -1]]

            # Crop the image to this bounding box
            image = image.crop((cmin, rmin, cmax, rmax))

            # Resize the image (pre-dither) using nearest neighbor
            size = (300, 300)  # Set your desired size here
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
            image = image.resize(post_size, Image.NEAREST)

            # Save the image with a new filename that includes the resolution
            new_filename = os.path.splitext(filename)[0] + f"_{post_size[0]}x{post_size[1]}.png"
            image.save(new_filename)
            print("Saving " + new_filename)

            # If new file is saved successfully, remove the original file
            if os.path.isfile(new_filename):
                os.remove(filename)
                print(f"Removed original file: {filename}")

        except Exception as e:
            print(f"An error occurred for file: {filename}. Error details: {str(e)}")

# Get a list of all files in the directory
files = os.listdir(input_folder)

# Loop over all files
for filename in files:
    # Check if the file is an image
    if filename.endswith('.png'):
        # Process the image
        process_image(os.path.join(input_folder, filename))
        print("Processed " + filename)

print("Image processing complete.")

