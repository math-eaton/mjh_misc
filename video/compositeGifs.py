from PIL import Image
import imageio
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
        # Convert to PIL Image
        pil_frame1 = Image.fromarray(frame1)
        pil_frame2 = Image.fromarray(frame2)

        # Make sure both images are in RGBA mode
        pil_frame1 = pil_frame1.convert("RGBA")
        pil_frame2 = pil_frame2.convert("RGBA")

        # Composite images
        composite_frame = Image.alpha_composite(pil_frame1, pil_frame2)

        # Append to output frames
        output_frames.append(composite_frame)

    # Save the output GIF
    imageio.mimsave(output_path, [frame.convert("RGBA") for frame in output_frames], 'GIF', duration=0.09, loop=0, disposal=2)

    print("done.")


gif_path1 = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/area_inverted.gif'
gif_path2 = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/polyline_images_inverted.gif'
output_path = '/Users/matthewheaton/Documents/GitHub/imagery_scraper/output/animations/area_combined_inverted.gif'
superimpose_gifs(gif_path1, gif_path2, output_path)
