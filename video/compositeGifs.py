import imageio
import numpy as np
from tqdm import tqdm

def superimpose_gifs(gif_path1, gif_path2, output_path):
    # Create readers for the GIFs
    reader1 = imageio.get_reader(gif_path1)
    reader2 = imageio.get_reader(gif_path2)

    # Check number of frames
    if reader1.get_length() != reader2.get_length():
        raise ValueError("GIFs must have the same number of frames")

    # Process each frame
    output_frames = []
    for frame1, frame2 in tqdm(zip(reader1, reader2), total=reader1.get_length(), desc="Processing frames"):
        # Ensure frames have an alpha channel
        if frame1.shape[2] == 3:
            frame1 = np.concatenate([frame1, np.full_like(frame1[..., :1], 255)], axis=2)
        if frame2.shape[2] == 3:
            frame2 = np.concatenate([frame2, np.full_like(frame2[..., :1], 255)], axis=2)

        # Normalize the alpha channel
        alpha1 = frame1[:, :, 3] / 255.0
        alpha2 = frame2[:, :, 3] / 255.0

        # Composite the RGB channels
        composite_rgb = alpha1[..., None] * frame1[:, :, :3] + (1 - alpha1[..., None]) * alpha2[..., None] * frame2[:, :, :3]

        # Combine the alpha channels
        composite_alpha = (alpha1 + (1 - alpha1) * alpha2) * 255

        # Create the final frame
        composite_frame = np.concatenate([composite_rgb, composite_alpha[..., None]], axis=2).astype(np.uint8)

        # Append to output frames
        output_frames.append(composite_frame)

    # Save the output GIF
    imageio.mimsave(output_path, output_frames, format='GIF', duration=0.09, loop=0, disposal=2)

    print("done.")

gif_path1 = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/area_inverted.gif'
gif_path2 = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/polyline_inverted.gif'
output_path = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/combined_inverted.gif'
superimpose_gifs(gif_path1, gif_path2, output_path)
