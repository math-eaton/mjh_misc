import arcpy

# Reference a project, map, and layer using arcpy.mp
p = arcpy.mp.ArcGISProject('current') 
m = p.listMaps('Map')[0]
lyr = m.listLayers('GreatLakes')[0]

# Get the layer's CIM definition
cim_lyr = lyr.getDefinition('V2')

# Make changes to field properties
for fd in cim_lyr.featureTable.fieldDescriptions:
    if fd.fieldName == "OBJECTID":
        fd.visible = False            #Do not display this field
    if fd.fieldName == "Shape_Area":
        fd.alias = "Area (hectares)"  #Change field alias

# Push the changes back to the layer object
lyr.setDefinition(cim_lyr)
