import arcpy

p = arcpy.mp.ArcGISProject('current')
m = p.listMaps('GreatLakes')[0]
l = m.listLayers('GreatLakes')[0]

l_cim = l.getDefinition('V3')         #Get layer's CIM / Layer URI
lURI = l_cim.uRI                      #Needed to specific the index layer 

lyt = p.listLayouts('GreatLakes')[0]
lyt_cim = lyt.getDefinition('V3')     #Get Layout's CIM definition

#Create CIM Spatial Map Series Object and populate its properties
ms = arcpy.cim.CreateCIMObjectFromClassName('CIMSpatialMapSeries', 'V3')
ms.enabled = True
ms.mapFrameName = "Great Lakes MF"
ms.startingPageNumber = 1
ms.currentPageID = 2
ms.indexLayerURI = lURI               #Index layer URI from Layer's CIM 
ms.nameField = "pageName"
ms.sortField = "NAME"
ms.sortAscending = True
ms.scaleRounding = 200
ms.extentOptions = "BestFit"
ms.marginType = "Percent"
ms.margin = 2

lyt_cim.mapSeries = ms                #Set new map series to layout
lyt.setDefinition(lyt_cim)            #Set the Layout's CIM definition

#Force a refresh of the layout and its associated panes
lyt_cim = lyt.getDefinition('V3')
lyt.setDefinition(lyt_cim)