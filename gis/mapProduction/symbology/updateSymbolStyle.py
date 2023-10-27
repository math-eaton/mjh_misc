import arcpy

# define project
# project_path = r"C:\Users\person\Desktop\folder\project.aprx"
p = arcpy.mp.ArcGISProject("CURRENT")

# specify map in project named "Map"
m = p.listMaps('Map')[0]

# specify layer in map named "polygons"
lyr = m.listLayers('polygons')[0]

# access symbology of layer and change symbology to graduated colors
sym = lyr.symbology
sym.updateRenderer('GraduatedColorsRenderer')
sym.renderer.classificationField = 'value'
sym.classificationMethod = 'NaturalBreaks'
sym.renderer.breakCount = 10

# save symbology back onto layer
lyr.symbology = sym

# save project
p.save()