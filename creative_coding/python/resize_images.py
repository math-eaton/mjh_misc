from PIL import Image
import os

# Define the image size (5.5 inches x 300 dpi)
image_size = (int(5.5 * 300), int(5.5 * 300))

# Define the input folder
input_folder = "/Users/matthewheaton/Documents/CIL_API_output"

# Function to resize an image
def resize_image(filename):
    try:
        # Load the image
        image = Image.open(filename)

        # Resize the image
        image = image.resize(image_size, Image.LANCZOS)

        # Save the image
        filename = os.path.splitext(filename)[0] + ".png"
        image.save(filename, "PNG")
    except Exception as e:
        print(f"An error occurred for file: {filename}. Error details: {str(e)}")

# Resize all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg"):
        resize_image(os.path.join(input_folder, filename))
