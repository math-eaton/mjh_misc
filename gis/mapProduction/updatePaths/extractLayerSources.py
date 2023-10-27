import arcpy
import csv
import json

# Set your workspace to the folder containing the project
arcpy.env.workspace = r"C:\Path\to\Your\Workspace"

# Access your ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("C:\Path\to\Your\Project.aprx")

# Create a list to store layer information
layer_info = []

# Iterate through the map(s) in your project
for map in aprx.listMaps():
    # Iterate through layers in the map
    for layer in map.listLayers():
        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            layer_info.append({
                "MapName": map.name,
                "LayerName": layer.name,
                "DataSource": layer.dataSource
            })

# Define the output file path (either CSV or JSON)
output_file = r"C:\Path\to\Your\Output\File.json"

# Save the layer information to the output file
with open(output_file, "w") as file:
    json.dump(layer_info, file, indent=4)  # Use json.dump for JSON output

# Alternatively, if you want to save it to a CSV file
# with open(output_file, "w", newline="") as file:
#     csv_writer = csv.DictWriter(file, fieldnames=["MapName", "LayerName", "DataSource"])
#     csv_writer.writeheader()
#     csv_writer.writerows(layer_info)