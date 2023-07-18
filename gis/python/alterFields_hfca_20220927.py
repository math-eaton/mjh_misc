#Import geoprocessing
import arcpy

#Set workspace
arcpy.env.workspace = r'D:\GRID\ZMB\Cartography\ZMB_EPI_COVAX_december_20211207\dynamic_tables_arcpy_20220927.gdb'

#Loop through feature classes looking for a field named 'elev'
fcList = arcpy.ListFeatureClasses() #get a list of feature classes
for fc in fcList:  #loop through feature classes
    fieldList = arcpy.ListFields(fc)  #get a list of fields for each feature class
    for field in fieldList: #loop through each field
        #### misc table

        if field.name == 'distance':
            arcpy.AlterField_management(fc, field.name, 'distance', 'Distance to nearest HF')

        #### grid3 numbers

        elif field.name == 'SUM_tot_pop':
            arcpy.AlterField_management(fc, field.name, 'SUM_tot_pop', 'Total pop')

        elif field.name == 'SUM_pop_12_17':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_12_17', 'Pop 12-17')

        elif field.name == 'SUM_pop_18_64':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_18_64', 'Pop 18-64')

        elif field.name == 'SUM_pop_above65': 
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_above65', 'Pop >65')

        elif field.name == 'SUM_pop_mf0_1':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_mf0_1', 'Pop <1')

        elif field.name == 'SUM_pop_under5':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_under5', 'Pop <5')

        elif field.name == 'SUM_pop_f9':  #look for the name
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_f9', 'Female pop 9')

        elif field.name == 'SUM_pop_f14':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_f14', 'Female pop 14')

        elif field.name == 'SUM_pop_f15_49':
            arcpy.AlterField_management(fc, field.name, 'SUM_pop_f15_49', 'Female pop 15-49')

        #### bottom up

        elif field.name == 'SUM_adj_tot_pop':
            arcpy.AlterField_management(fc, field.name, 'SUM_adj_tot_pop', 'Total pop')

        elif field.name == 'SUM_topdown_12_17':
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_12_17', 'Pop 12-17')

        elif field.name == 'SUM_topdown_18_64':
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_18_64', 'Pop 18-64')

        elif field.name == 'SUM_topdown_above65': 
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_above65', 'Pop >65')

        elif field.name == 'SUM_topdown_mf0_1':
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_mf0_1', 'Pop <1')

        elif field.name == 'SUM_adj_pop_under5':
            arcpy.AlterField_management(fc, field.name, 'SUM_adj_pop_under5', 'Pop <5')

        elif field.name == 'SUM_topdown_f9':  #look for the name
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_f9', 'Female pop 9')

        elif field.name == 'SUM_topdown_f14':
            arcpy.AlterField_management(fc, field.name, 'SUM_topdown_f14', 'Female pop 14')

        elif field.name == 'SUM_adj_pop_f15_49':
            arcpy.AlterField_management(fc, field.name, 'SUM_adj_pop_f15_49', 'Female pop 15-49')

        #### district sums
        #### grid3 numbers district

        elif field.name == 'SUM_SUM_tot_pop':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_tot_pop', 'Total pop')

        elif field.name == 'SUM_SUM_pop_12_17':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_12_17', 'Pop 12-17')

        elif field.name == 'SUM_SUM_pop_18_64':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_18_64', 'Pop 18-64')

        elif field.name == 'SUM_SUM_pop_above65': 
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_above65', 'Pop >65')

        elif field.name == 'SUM_SUM_pop_mf0_1':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_mf0_1', 'Pop <1')

        elif field.name == 'SUM_SUM_pop_under5':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_under5', 'Pop <5')

        elif field.name == 'SUM_SUM_pop_f9':  #look for the name
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_f9', 'Female pop 9')

        elif field.name == 'SUM_SUM_pop_f14':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_f14', 'Female pop 14')

        elif field.name == 'SUM_SUM_pop_f15_49':
            arcpy.AlterField_management(fc, field.name, 'SUM_SUM_pop_f15_49', 'Female pop 15-49')

        # #### bottom up district

        # elif field.name == 'SUM_SUM_adj_tot_pop':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_adj_tot_pop', 'Total pop')

        # elif field.name == 'SUM_SUM_topdown_12_17':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_12_17', 'Pop 12-17')

        # elif field.name == 'SUM_SUM_topdown_18_64':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_18_64', 'Pop 18-64')

        # elif field.name == 'SUM_SUM_topdown_above65': 
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_above65', 'Pop >65')

        # elif field.name == 'SUM_SUM_topdown_mf0_1':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_mf0_1', 'Pop <1')

        # elif field.name == 'SUM_SUM_adj_pop_under5':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_adj_pop_under5', 'Pop <5')

        # elif field.name == 'SUM_SUM_topdown_f9':  #look for the name
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_f9', 'Female pop 9')

        # elif field.name == 'SUM_SUM_topdown_f14':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_topdown_f14', 'Female pop 14')

        # elif field.name == 'SUM_SUM_adj_pop_f15_49':
        #     arcpy.AlterField_management(fc, field.name, 'SUM_SUM_adj_pop_f15_49', 'Female pop 15-49')

    else :
        print("all done!")