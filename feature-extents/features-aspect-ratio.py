# Write aspect ratio to new field in same feature class
# Taken from GeoNet user csny490 (https://community.esri.com/thread/92651)
# Demonstrates how to work with cursors and work with shapes of data and update attributes.
featureClass = "D:/working_files/data.gdb/Counties"
arcpy.AddField_management(featureClass, "ASP_RATIO", "DOUBLE")
updateRows = arcpy.da.UpdateCursor(featureClass, ["SHAPE@", "ASP_RATIO"])
for updateRow in updateRows:
	shapeObj = updateRow[0]
	x1,y1,x2,y2,x3,y3,x4,y4 = [float(coord) for coord in shapeObj.hullRectangle.split(" ")]
	distance1 = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	distance2 = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
	if distance1 <= distance2:
		updateRow[1] = distance2 / distance1
	else:
		updateRow[1] = distance1 / distance2
	updateRows.updateRow(updateRow)
del updateRow, updateRows
