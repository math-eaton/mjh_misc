import os
import json

folder_path = "/Users/matthewheaton/Documents/GitHub/cdp_colloquium_i/assets/fiction"  # Replace this with the path to your image folder
image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

data = {"images": image_files}

with open("images.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file 'images.json' created successfully.")
