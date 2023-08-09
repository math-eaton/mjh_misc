import os
import subprocess
from PIL import Image
from tqdm import tqdm

def convert_mov_to_gif(input_mov, output_gif, resize=(536, 383), frame_rate=10):
    # Create a temporary directory for frames
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Convert the MOV to individual frames using ffmpeg
    subprocess.call([
        'ffmpeg',
        '-i', input_mov,
        '-r', str(frame_rate),  # Frame rate
        os.path.join(temp_dir, 'frame%04d.png')
    ])
    
    # Read all the frames
    frame_files = sorted([os.path.join(temp_dir, f) for f in os.listdir(temp_dir)])
    frames = [Image.open(f).convert('RGBA').resize(resize, Image.NEAREST) for f in tqdm(frame_files, desc="Reading frames")]
    
    # Save as a GIF
    frames[0].save(output_gif, save_all=True, append_images=frames[1:], optimize=True, duration=1000//frame_rate, loop=0)

    # Cleanup temporary directory
    for frame_file in frame_files:
        os.remove(frame_file)
    os.rmdir(temp_dir)

    print("Conversion done.")


input_mov = "/Users/matthewheaton/Desktop/screenshot/Screen Recording 2023-08-09 at 5.39.02 PM.mov" 
output_gif = "/Users/matthewheaton/Documents/GitHub/cdp_colloquium_i/site_refactor/assets/gif/WFH_DJ.gif" 

convert_mov_to_gif(input_mov, output_gif)
