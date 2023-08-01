import pandas as pd
import arcpy
from shapely.geometry import Point, Polygon
from math import radians, sin, cos

# Function to convert coordinates
def convert_coordinates(center, az, distance):
    lat1, lon1 = map(radians, center)
    bearing = radians(az)
    
    lat2 = asin(sin(lat1)*cos(distance) + cos(lat1)*sin(distance)*cos(bearing))
    lon2 = lon1 + atan2(sin(bearing)*sin(distance)*cos(lat1), cos(distance)-sin(lat1)*sin(lat2))
    
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    return lat2, lon2

# Load data
df = pd.read_csv('file.csv', delimiter='|')

# Create empty lists to store geometries
polygons = []
points = []

# Loop over DataFrame
for i, row in df.iterrows():
    # Extract transmitter site
    transmitter_site = [float(x) for x in row['transmitter_site'].split(',')]
    points.append(Point(transmitter_site))
    
    # Convert azimuthal coordinates to polygon vertices
    vertices = []
    for az in range(360):
        distance = row[str(az)]
        vertex = convert_coordinates(transmitter_site, az, distance)
        vertices.append(vertex)
    
    # Create Polygon
    polygons.append(Polygon(vertices))

# Create Spatial DataFrame for points and save as Shapefile
sdf_points = pd.DataFrame.spatial.from_xy(df, 'longitude', 'latitude')
sdf_points.spatial.to_featureclass(location=r'C:\path\to\output\points.shp')

# Create Spatial DataFrame for polygons and save as Shapefile
sdf_polygons = pd.DataFrame.spatial.from_geometry(polygons)
sdf_polygons.spatial.to_featureclass(location=r'C:\path\to\output\polygons.shp')
