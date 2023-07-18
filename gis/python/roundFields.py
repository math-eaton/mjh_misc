import arcpy

arcpy.env.workspace = r'D:\GRID\ZMB\Cartography\ZMB_EPI_COVAX_december_20211207\dynamic_tables_arcpy_20220927.gdb'

fcList = arcpy.ListFeatureClasses() #get a list of feature classes
print(fcList)
for fc in fcList:  #loop through feature classes
    fieldList = arcpy.ListFields(fc, "", "Double")  #get a list of fields for each feature class
    print(fieldList)

    for field in fieldList:

        with arcpy.da.UpdateCursor(fc, "*") as cursor:
            for row in cursor:
                if row[0] is None:
                    pass
                else:
                    row[0] = round(float(row[0]), 0)  # Uses float() in case fieldname is a string            
                    cursor.updateRow(row)
                    print('updated value to {}'.format(row[0]))

        arcpy.AddField_management(table, "Rounded", 'DOUBLE')
        with arcpy.da.UpdateCursor(table, ["Distance", "Rounded"]) as cursor:
            for row in cursor:
                row[1] = round(float(row[0]), 3)
                cursor.updateRow(row)

    print("fc done")

print('all done!')