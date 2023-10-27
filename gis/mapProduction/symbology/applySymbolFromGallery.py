import arcpy, os, sys
relpath = os.path.dirname(sys.argv[0])

p = arcpy.mp.ArcGISProject(os.path.join(relpath, "Symbol.aprx"))
m = p.listMaps('Map')[0]
lyr = m.listLayers("Study Areas")[0]
sym = lyr.symbology

sym.renderer.symbol.applySymbolFromGallery("Extent Transparent Wide Gray")
sym.renderer.symbol.color = {'RGB' : [255, 0, 0, 60]}
sym.renderer.symbol.outlineColor = {'CMYK' : [25, 50, 75, 25, 100]}
sym.renderer.symbol.size = 3

lyr.symbology = sym

p.saveACopy(os.path.join(relpath, "SavedOutput.aprx"))