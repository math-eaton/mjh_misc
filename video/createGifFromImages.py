import os
import imageio.v2 as imageio
from tqdm import tqdm
from PIL import Image, ImageSequence

def create_gif(image_files, gif_path):
    # Open images
    images = [imageio.imread(x) for x in tqdm(image_files, desc="Reading images")]

    # Save images as a GIF
    imageio.mimsave(gif_path, images, 'GIF', duration=0.09, oopl=1, disposal=2)

    print("done.")



def create_gif_batch(image_files, gif_path, batch_size=500):
    # Determine the number of batches
    num_batches = len(image_files) // batch_size
    temp_gifs = []

    for i in tqdm(range(num_batches + 1), desc="Processing batches"):
        # Create a batch of images
        batch_images = image_files[i * batch_size: (i + 1) * batch_size]
        if not batch_images:
            continue
        # Read images
        images = [imageio.imread(x, mode='RGBA') for x in tqdm(batch_images, desc="Reading images", leave=False)]
        
        # Create a temporary GIF for this batch
        temp_gif_path = f"temp_{i}.gif"
        imageio.mimsave(temp_gif_path, images, 'GIF', duration=0.09, oopl=1, disposal=2)
        temp_gifs.append(temp_gif_path)

    # Open the first temporary GIF to get its size
    # first_gif = Image.open(temp_gifs[0])
    final_gif_frames = []

    # Iterate over the temporary GIFs, opening each one and appending its frames to the final GIF
    for temp_gif in tqdm(temp_gifs, desc="Concatenating GIFs"):
        with Image.open(temp_gif) as img:
            for frame in ImageSequence.Iterator(img):
                # Copy each frame to ensure proper disposal
                final_frame = frame.copy()
                final_gif_frames.append(final_frame)

    # Save the final GIF with the proper disposal method
    final_gif_frames[0].save(gif_path, save_all=True, append_images=final_gif_frames[1:], duration=90, loop=0, disposal=2)

    # Remove temporary GIFs
    for temp_gif in temp_gifs:
        os.remove(temp_gif)

    print("done.")

image_folder = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/processed_imagery/point' 
image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])

# Take the first 100 images for testing results
image_files = image_files[:250]

gif_path = "/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/point.gif"
create_gif(image_files, gif_path)
# create_gif_batch(image_files, gif_path)