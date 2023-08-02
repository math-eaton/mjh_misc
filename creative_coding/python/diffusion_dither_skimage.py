from PIL import Image
import numpy as np
import os
from skimage.io import imread, imsave
from skimage.color import rgb2gray, rgb2gray
from skimage.util import img_as_ubyte
from skimage.transform import resize
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage import filters

# Define the directory with the images
input_folder = "/Users/matthewheaton/Documents/CIL_API_output"

@adapt_rgb(each_channel)
def dithering_floyd_steinberg(image):
    rng = np.random.default_rng(12345)
    image = img_as_ubyte(image) / 255.  # Convert to float in range [0, 1]
    err = rng.normal(0, 0.1, size=image.shape) / 255.  # Ensure err is also in range [0, 1]
    image = np.clip(image + err, 0, 1)  # Clip values to be within [0, 1]
    binary = image > 0.5
    err = image - binary.astype(float)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            nb = err[i, j] / 16
            if i + 1 < image.shape[0]:
                err[i + 1, j] += 7 * nb
                if j + 1 < image.shape[1]:
                    err[i + 1, j + 1] += nb
                if j - 1 >= 0:
                    err[i + 1, j - 1] += 3 * nb
            if j + 1 < image.shape[1]:
                err[i, j + 1] += 5 * nb
    return binary

def process_image(filename):
    # Load the image
    image = Image.open(filename)

    # Convert the image to grayscale
    image = image.convert('L')

    # Convert the image to a NumPy array
    image = np.array(image) / 255.  # Convert to float in range [0, 1]

    # Dither the image using the Floyd-Steinberg algorithm
    image = dithering_floyd_steinberg(image)

    # Convert the image back to PIL Image and RGB mode
    image = Image.fromarray((image * 255).astype(np.uint8)).convert('RGB')

    # If the image is not in RGBA mode, convert it to RGBA
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Convert the image data to a NumPy array
    data = np.array(image)

    # Create a mask of all white (also shades of whites) pixels
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    white_areas = (red > 200) & (green > 200) & (blue > 200)

    # Change all white (also shades of whites) pixels to transparent
    data[white_areas.T] = [255, 255, 255, 0]

    # Create a new Image object from the data
    image = Image.fromarray(data)

    # Save the image
    image.save(filename)

# Get a list of all files in the directory
files = os.listdir(input_folder)

# Loop over all files
for filename in files:
    # Check if the file is an image
    if filename.endswith('.png'):
        # Process the image
        process_image(os.path.join(input_folder, filename))
