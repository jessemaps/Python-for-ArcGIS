# Write aspect ratio to new field in same feature class
# Taken from GeoNet user csny490 (https://community.esri.com/thread/92651)
# Demonstrates how to work with cursors and work with shapes of data and update attributes.
featureClass = "D:/working_files/data.gdb/Counties"
arcpy.AddField_management(featureClass, "ASP_RATIO", "DOUBLE")
updateRows = arcpy.da.UpdateCursor(featureClass, ["SHAPE@", "ASP_RATIO"])
for updateRow in updateRows:
	shapeObj = updateRow[0]
	width = shapeObj.extent.XMax - shapeObj.extent.XMin
	height = shapeObj.extent.YMax - shapeObj.extent.YMin
	if width <= height:
		updateRow[1] = height / width
	else:
		updateRow[1] = width / height
	updateRows.updateRow(updateRow)
del updateRow, updateRows
