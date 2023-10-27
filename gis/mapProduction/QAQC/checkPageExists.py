import arcpy
import csv
import os

# Set up workspace and input feature class
workspace = r'C:\path\to\your\workspace'  # Replace with the path to your ArcGIS workspace
arcpy.env.workspace = workspace
feature_class = 'your_polygon_feature_class'  # Replace with the name of your feature class
output_csv = 'output.csv'  # Replace with the desired CSV file name

# Extract records from the "pageName" field and export as CSV
field_name = 'pageName'
records = []
with arcpy.da.SearchCursor(feature_class, field_name) as cursor:
    for row in cursor:
        records.append(row[0])

# Export the records to a CSV file
with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([field_name])  # Write the header
    for record in records:
        csv_writer.writerow([record])

# Define the directory with filenames to check against
file_directory = r'C:\path\to\your\file\directory'  # Replace with the path to your directory

# Check records against filenames and output mismatched names
mismatched_records = []
for record in records:
    filename = record + '.txt'  # Assuming record names correspond to file names with ".txt" extension
    file_path = os.path.join(file_directory, filename)
    if not os.path.exists(file_path):
        mismatched_records.append(record)

# Output the mismatched records to a text file
output_text_file = 'mismatched_records.txt'
with open(output_text_file, 'w') as text_file:
    text_file.write("Records with no corresponding files:\n")
    for record in mismatched_records:
        text_file.write(record + '\n')

print("Script completed. Mismatched records have been saved to", output_text_file)
