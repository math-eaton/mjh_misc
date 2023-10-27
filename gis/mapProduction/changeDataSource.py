import arcpy
import os

oldDataset = 'PtsInterest'
newDataset = 'PointsOfInterest'
fGDB = r'C:\Projects\YosemiteNP\Yosemite.gdb'

aprx = arcpy.mp.ArcGISProject(r'C:\Projects\YosemiteNP\Yosemite.aprx')

for m in aprx.listMaps():
    for lyr in m.listLayers():
        if lyr.supports("DATASOURCE"):
            if lyr.dataSource == os.path.join(fGDB, oldDataset):
                lyr.updateConnectionProperties({'dataset': oldDataset}, {'dataset': newDataset})
                
aprx.saveACopy(r"C:\Projects\YosemiteNP\YosemiteNew.aprx")
