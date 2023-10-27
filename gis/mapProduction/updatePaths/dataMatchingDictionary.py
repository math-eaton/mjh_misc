import arcpy

# Set your workspace to the folder containing the new geodatabase
arcpy.env.workspace = r"C:\Path\to\Your\Workspace"

# Define the path to your new geodatabase
new_geodatabase = r"C:\Path\to\Your\New\Geodatabase.gdb"

# Create a dictionary to map old feature class names to new data sources
data_source_mapping = {
    "OldLayer1": new_geodatabase + "\\NewFeatureClass1",
    "OldLayer2": new_geodatabase + "\\NewFeatureClass2",
    # Add more mappings as needed
}

# Access your ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("C:\Path\to\Your\Project.aprx")

# Iterate through the map(s) in your project
for map in aprx.listMaps():
    # Create a list to store the layer names and data source paths
    layer_info = []

    # Iterate through layers in the map
    for layer in map.listLayers():
        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            old_data_source = layer.dataSource
            new_data_source = data_source_mapping.get(layer.name)

            if new_data_source:
                # Update the layer's data source
                layer.updateConnectionProperties(layer.connectionProperties, new_data_source)
                layer_info.append((layer.name, old_data_source, new_data_source))

    # Print the layer information for this map
    print(f"Layers updated in map '{map.name}':")
    for name, old_source, new_source in layer_info:
        print(f"  Layer Name: {name}")
        print(f"  Old Data Source: {old_source}")
        print(f"  New Data Source: {new_source}")
        print()

# Save the changes to your project
aprx.save()