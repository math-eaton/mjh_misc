import arcpy
import os

# arcpy.env.overwriteOutput = True 

workspace = "D:\GRID\MOZ\MOZ_COVAX_microplanning_v2_1_20220920\dissolves\dissolves_scratch"
outdir = "D:\GRID\MOZ\MOZ_COVAX_microplanning_v2_1_20220920\dissolves\merged.gdb"

walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polygon")
di = {}

for dirpath, dirnames, filenames in walk:
          for filename in filenames:
             fcFullPath = os.path.join(dirpath, filename)
            #  print filename
            #  print fcFullPath
             #try adding feature class to dictionary with already-existing key
             try: di [filename] += [fcFullPath]
             #key not in dictionary yet. Create key
             except: di [filename] = [fcFullPath]



#iterate dictionary
for filename in di:
    #get merge feature classes and print output filename from dict
    print(filename)
    mergeFcs = di [filename]
    output = os.path.join(outdir, filename + "_merge")
    arcpy.Merge_management(mergeFcs, output)