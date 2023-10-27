import arcpy

aprx = arcpy.mp.ArcGISProject(r"C:\Projects\YosemiteNP\Yosemite.aprx")
for m in aprx.listMaps():
    print("Map: {0} Layers".format(m.name))
    for lyr in m.listLayers():
        if lyr.isBroken:
            print("(BROKEN) " + lyr.name)
        else:
            print("  " + lyr.name)
del aprx
