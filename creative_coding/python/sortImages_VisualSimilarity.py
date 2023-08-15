import os
import cv2
import shutil
from tqdm import tqdm

def preprocess_images(input_dir, standard_size=(1200, 1200)):
    """Preprocess images to a standard resolution and color space with transparency support."""
    all_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Preprocessing {len(all_files)} images...")
    
    for filename in tqdm(all_files):
        filepath = os.path.join(input_dir, filename)
        img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # Load image with all channels including alpha
        
        # Check the number of channels
        # If it's 2, it's grayscale with alpha
        # If it's 3, it's RGB without alpha
        # If it's 4, it's RGBA
        channels = img.shape[2] if len(img.shape) == 3 else 1

        # Convert grayscale to RGB (without alpha) or RGBA (with alpha)
        if channels == 2:
            img_rgb = cv2.cvtColor(img[:, :, :1], cv2.COLOR_GRAY2BGR)
            img = cv2.merge([img_rgb, img[:, :, 1]])
        elif channels == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        img_resized = cv2.resize(img, standard_size)
        cv2.imwrite(filepath, img_resized)
    
    print("Preprocessing completed!")

def copy_and_rename(image_path, idx, output_folder):
    """Copy the image to the output folder and rename it based on the index."""
    new_name = os.path.join(output_folder, f"frame_{idx}.png")
    shutil.copy(image_path, new_name)

def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    _, des = orb.detectAndCompute(img, None)
    return des

def compute_similarity(des1, des2):
    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        return float('inf')

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Using the sum of distances as the score
    return sum([m.distance for m in matches])

def sort_images_by_similarity(seed_image_path, image_folder):
    # Extract features from the seed image
    seed_features = extract_features(seed_image_path)
    print("Extracting features from the seed image...")

    
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.png')]
    
    # Compute similarity scores
    scores = []
    print("Computing similarity scores for all images...")
    for image_path in tqdm(images):
        img_features = extract_features(image_path)
        similarity = compute_similarity(seed_features, img_features)
        scores.append((image_path, similarity))
    
    # Sort based on scores
    sorted_images = sorted(scores, key=lambda x: x[1], reverse=False)
    
    return [img[0] for img in sorted_images]

def main(image_folder, output_folder):
    # Preprocess images before sorting
    preprocess_images(image_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = os.listdir(image_folder)
    seed_image_path = os.path.join(image_folder, images[0])
    sorted_image_paths = sort_images_by_similarity(seed_image_path, image_folder)
    
    print("Copying and renaming the images based on similarity...")
    for idx, image_path in tqdm(enumerate(sorted_image_paths)):
        copy_and_rename(image_path, idx, output_folder)
    
    print("done.")

if __name__ == "__main__":
    folder_path = "/Users/matthewheaton/Documents/CIL_unprocessed"
    output_path = "/Users/matthewheaton/Documents/CIL_unprocessed_sort"
    main(folder_path, output_path)
