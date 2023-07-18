import arcpy
from arcpy import env

# Set environment settings
env.workspace = "path/to/your/geodatabase.gdb"  # Replace with your Geodatabase path

# Set the local variables
joinFeatures = "your_join_features"  # Replace with your join feature class
join_field = "page_name"  # Field to join

# Create a new field 'page_name' in the join feature class
arcpy.AddField_management(joinFeatures, join_field, "TEXT")

# Concatenate 'statename', 'lganame', and 'wardname' fields with an underscore separator
arcpy.CalculateField_management(joinFeatures, join_field, "!statename! + '_' + !lganame! + '_' + !wardname!", "PYTHON3")

# Define a function to remove non-ascii characters and replace spaces with hyphens
code_block = """
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128).replace(' ', '-')
"""

# Apply the function to the 'page_name' field
arcpy.CalculateField_management(joinFeatures, join_field, "remove_non_ascii(!{}!)".format(join_field), "PYTHON3", code_block)

# Get a list of all feature classes
featureclasses = arcpy.ListFeatureClasses()

# Loop through each feature class
for targetFeatures in featureclasses:
    outfc = f"{targetFeatures}_joined"  # Each output feature will have a unique name

    # Use the Spatial Join tool to join the two feature classes.
    arcpy.analysis.SpatialJoin(targetFeatures, joinFeatures, outfc)

    # Now, let's iterate through other feature classes and join the 'page_name' field to them
    for fc in featureclasses:
        if fc != targetFeatures:  # Avoid joining the target feature class with itself
            # Add Join Field
            arcpy.management.AddJoin(fc, "OBJECTID", outfc, "TARGET_FID")

            # Copy the joined field to a new field in the feature class
            arcpy.management.CalculateField(fc, join_field, "!{}.{}!".format(outfc, join_field), "PYTHON3")

            # Remove Join
            arcpy.management.RemoveJoin(fc, outfc)
