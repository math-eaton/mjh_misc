#Import geoprocessing
import arcpy

#Set workspace
arcpy.env.workspace = r'D:\GRID\ZMB\Cartography\ZMB_EPI_COVAX_december_20211207\dynamic_tables_arcpy2_20220927.gdb'

#Loop through feature classes looking for a field named 'elev'
fcList = arcpy.ListFeatureClasses() #get a list of feature classes
for fc in fcList:  #loop through feature classes
    fieldList = arcpy.ListFields(fc)  #get a list of fields for each feature class
    for field in fieldList: #loop through each field
        #### misc table

        if field.name == 'distance':
            arcpy.AlterField_management(fc, field.name, 'distance', 'Distance to nearest HF')

        # #### grid3 numbers

        elif field.name == 'SUM_tot_pop':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Total pop')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_tot_pop!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_12_17':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop 12-17')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_12_17!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_18_64':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop 18-64')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_18_64!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_above65':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop >65')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_above65!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_mf0_1':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop <1')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_mf0_1!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_under5':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop <5')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_under5!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_f9':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 9')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_f9!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_f14':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 14')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_f14!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_pop_f15_49':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 15-49')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_pop_f15_49!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        # #### bottom up

        elif field.name == 'SUM_adj_tot_pop':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Total pop')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_adj_tot_pop!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_12_17':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop 12-17')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_12_17!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_18_64':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop 18-64')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_18_64!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_above65':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop >65')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_above65!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_mf0_1':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop <1')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_mf0_1!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_adj_pop_under5':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Pop <5')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_adj_pop_under5!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_f9':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 9')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_f9!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_topdown_f14':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 14')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_topdown_f14!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        elif field.name == 'SUM_adj_pop_f15_49':
            arcpy.AddField_management(fc, field.name+"_rounded", "LONG", "", "", "", 'Female pop 15-49')                    
            arcpy.CalculateField_management(fc, field.name+"_rounded", "!SUM_adj_pop_f15_49!", "PYTHON_9.3", "")
            arcpy.DeleteField_management(fc, field.name)

        else :
            print("field complete!")
            #print('updated value to{}'.format(row[0]))

    print("fc complete!")

print("all done!!")