from PIL import Image
import imageio
from tqdm import tqdm

def superimpose_gifs(gif_path1, gif_path2, output_path, alpha=0.5):
    # Read the GIFs
    gif1 = imageio.mimread(gif_path1)
    gif2 = imageio.mimread(gif_path2)

    # Make sure the GIFs have the same number of frames
    if len(gif1) != len(gif2):
        raise ValueError("GIFs must have the same number of frames")

    # Process each frame
    output_frames = []
    for frame1, frame2 in tqdm(zip(gif1, gif2), total=len(gif1), desc="Processing frames"):
        # Convert to PIL Image
        pil_frame1 = Image.fromarray(frame1)
        pil_frame2 = Image.fromarray(frame2)

        # Superimpose with blending
        blended_frame = Image.blend(pil_frame1, pil_frame2, alpha=alpha)

        # Append to output frames
        output_frames.append(blended_frame)

    # Save the output GIF
    imageio.mimsave(output_path, [frame.convert("RGBA") for frame in output_frames], 'GIF', duration=0.1)

    print("done.")

# Usage:
gif_path1 = 'path/to/first.gif'
gif_path2 = 'path/to/second.gif'
output_path = 'path/to/output.gif'
superimpose_gifs(gif_path1, gif_path2, output_path, alpha=0.5)
