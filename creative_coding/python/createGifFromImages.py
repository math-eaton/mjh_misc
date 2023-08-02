import os
import imageio.v2 as imageio

def create_gif(image_files, gif_path):
    # Open images
    images = [imageio.imread(x) for x in image_files]

    # Save images as a GIF
    imageio.mimsave(gif_path, images, 'GIF', duration=0.5)

image_folder = '/Users/matthewheaton/Documents/DOCENTS/lp1_design/assets/CIL_gif_sample' 
image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])

gif_path = "/Users/matthewheaton/Documents/DOCENTS/lp1_design/assets/cell_sample.gif"
create_gif(image_files, gif_path)
print("done.")
