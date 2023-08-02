import requests
from PIL import Image
from io import BytesIO
import os
import random
import time
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


# Record the start time
start_time = time.time()

# Define the number of images to download
num_images = 10

# Define the output folder
output_folder = "/Users/matthewheaton/Documents/DOCENTS/lp1_design/assets/CIL_square_images"

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

# Identify and crop any letterbox around the image
# higher sensitivity considers more grey values +/- 0 to 255 aka pure white/black
def crop_image(image, sensitivity=1):
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

# Assess the qualities of an image before dithering
def calculate_brightness(image):
    try:
        grayscale = image.convert('L')
        histogram = grayscale.histogram()
        pixels = sum(histogram)
        brightness = scale = len(histogram)

        for index in range(0, scale):
            ratio = histogram[index] / pixels
            brightness += ratio * (-scale + index)

        return 1 if brightness == 255 else brightness / scale

    except Exception as e:
        print(f"An error occurred in calculate_brightness: {str(e)}")
        return None

def calculate_contrast(image):
    try:
        grayscale = image.convert('L')
        grayscale_array = np.array(grayscale)
        contrast = grayscale_array.std()

        return contrast

    except Exception as e:
        print(f"An error occurred in calculate_contrast: {str(e)}")
        return None
    
def calculate_entropy(image):
    try:
        # Convert the image to grayscale
        grayscale = image.convert('L')
        
        # Calculate the histogram
        histogram = grayscale.histogram()

        # Normalize the histogram to get probabilities
        histogram_length = sum(histogram)
        probability_histogram = [float(h) / histogram_length for h in histogram]

        # Calculate entropy
        entropy = -sum([p * np.log2(p) for p in probability_histogram if p != 0])

        print("Assessing image qualities...")
        return entropy

    except Exception as e:
        print(f"An error occurred in calculate_entropy: {str(e)}")
        return None


# Process the image using Floyd-Steinberg error diffusion
def process_image(image):
    # Resize the image (pre-dither) while maintaining aspect ratio
    size = (1200, 1200)  # Set your desired size here
    image.thumbnail(size, Image.NEAREST)
    
    # Crop the image to desired aspect ratio (1:1 in this case)
    width, height = image.size
    new_size = min(width, height)

    left = (width - new_size)/2
    top = (height - new_size)/2
    right = (width + new_size)/2
    bottom = (height + new_size)/2

    # Calculate and print the aspect ratio
    aspect_ratio = new_size / new_size  # e.g. square is 1.0

    image = image.crop((left, top, right, bottom))
    print(f"Cropping to aspect ratio {aspect_ratio}")

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

    # Crop the outer 2%
    width, height = image.size
    left = width * 0.02
    top = height * 0.02
    right = width * 0.98
    bottom = height * 0.98
    image = image.crop((left, top, right, bottom))

    # Resize the image (post-dither) using nearest neighbor
    size = (1600, 1600)  # Set your desired size here
    # size = (1200, 900)  # Size for video
    image = image.resize(size, Image.NEAREST)
    print("Rescaling...")

    return image

# Configure retries
retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def download_image(image_id):
    try:
        # Fetch the document data from the API
        response = http.get(f"{api_url}/public_documents/{image_id}", auth=(username, password))
        response.raise_for_status()
        data = response.json()

        image_url = None

        # Check the ID type
        if image_id.startswith("CCDB_"):
            # Check each field
            for field in ccdb_fields:
                # Get the image URL from the API response
                image_url = data.get(field)
                if image_url:
                    break

        elif image_id.startswith("CIL_"):
            # Remove the "CIL_" prefix
            id_number = image_id[4:]

            # Construct the image URL
            image_url = f"https://cildata.crbs.ucsd.edu/media/thumbnail_display/{id_number}/{id_number}_thumbnailx512.jpg"

        if image_url is not None:
            # Fetch the image data
            response = requests.get(image_url, stream=True, timeout=5)
            response.raise_for_status()

            # Load the image data with PIL
            image = Image.open(BytesIO(response.content))

            # Crop the image
            image = crop_image(image)



            # Calculate the brightness, contrast, and entropy
            # BRIGHTNESS 0-1
            brightness = calculate_brightness(image)
            # CONTRAST 1-255
            contrast = calculate_contrast(image)
            # ENTROPY 1-8
            entropy = calculate_entropy(image)

            # Print the brightness, contrast, and entropy
            print(f"Brightness: {brightness}, Contrast: {contrast}, Entropy: {entropy}")

            # Check the image against your thresholds
            if brightness < 0.75 and contrast > 10 and entropy < 7:
                # Process the image
                image = process_image(image)

                # Save the image
                filename = os.path.join(output_folder, f"{image_id}_{image.size[0]}x{image.size[1]}.png")
                image.save(filename, "PNG")

                print("Image passed threshold, proceed.")
                return True

    except requests.exceptions.Timeout:
        print(f"Request timed out for image ID: {image_id}. Please check your network connection.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Image not found for ID: {image_id}")
        elif e.response.status_code == 429:
            print(f"Rate limit exceeded for image ID: {image_id}. Please wait before sending more requests.")
        else:
            print(f"HTTP error occurred for image ID: {image_id}. Error details: {str(e)}")

    except Exception as e:
        print(f"An error occurred for image ID: {image_id}. Error details: {str(e)}")

    return False

# alternatively, use a seed for pseudo-random ID shuffle
# random.seed(666)
# random.shuffle(ids)

# Fetch the list of public IDs
response = requests.get(f"{api_url}/public_ids?from=0&size=50000", auth=(username, password))
response.raise_for_status()

# Get the list of IDs
ids = [hit['_id'] for hit in response.json()['hits']['hits']]

# Randomly shuffle the list of IDs
# with new seed for random based on current time
random.seed(time.time())
random.shuffle(ids)

# Initialize counter for downloaded images
downloaded_images = 0

# Initialize an index for the IDs list
index = 0

while downloaded_images < num_images and index < len(ids):
    # Try to download the image at the current index
    if download_image(ids[index]):
        # If the download was successful, increment the counter
        downloaded_images += 1
        print(f"Downloading... ({downloaded_images} of {min(num_images, len(ids))})")
    # Always increment the index, whether the download was successful or not
    index += 1

print("Done.")
# Record the end time
end_time = time.time()

# Calculate and print the total execution time
total_time_sec= end_time - start_time
total_time_min=total_time_sec/60
print(f"Total runtime: {round(total_time_min, 2)} minutes")
