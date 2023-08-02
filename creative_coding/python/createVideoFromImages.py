import cv2
import os
from PIL import Image
import numpy as np

def create_video(image_files, video_path, fps, alpha_color=(255, 255, 255)):
    # Determine the width and height from the first image
    frame = Image.open(image_files[0])
    frame = frame.convert("RGBA")
    frame = Image.alpha_composite(Image.new("RGBA", frame.size, alpha_color), frame)
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGBA2BGR)

    height, width, channels = frame.shape

    # Define the codec and create a VideoWriter object
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in image_files:
        img = Image.open(image)
        img = img.convert("RGBA")
        img = Image.alpha_composite(Image.new("RGBA", img.size, alpha_color), img)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGR)
        video.write(img)

    video.release()

image_folder = '/Users/matthewheaton/Documents/DOCENTS/lp1_design/assets/CIL_gif_sample'
image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])

video_path = "/Users/matthewheaton/Documents/DOCENTS/lp1_design/assets/cell_sample.mp4"
fps = 16.0  # frames per second
create_video(image_files, video_path, fps, alpha_color=(255, 255, 255))  # white background
print("done.")
