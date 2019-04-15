# Create hull rectangles from input feature class. 
# Adapted from sample on GeoNet from user csny490 (https://community.esri.com/thread/92651) 
# Hull rectangles are different from envelopes in that they're rotated/oriented so longest side is parallel with widest section of shape.
# These Hull rectangles don't have attributes, so you have to later add the attributes by joining to the original data by object ID.
from arcpy import env

# Update variables to match project data:
featureClass = "D:/working_files/data.gdb/Counties"
env.workspace = "D:/working_files/data.gdb"
outputFeatureClass = "County_HullRectangles"
hullRectangles = []
updateRows = arcpy.da.UpdateCursor(featureClass, ["SHAPE@", "ASP_RATIO"])
for updateRow in updateRows:
	shapeObj = updateRow[0]
	x1,y1,x2,y2,x3,y3,x4,y4 = [float(coord) for coord in shapeObj.hullRectangle.split(" ")]
	pnt1 = arcpy.Point(x1,y1)
	pnt2 = arcpy.Point(x2,y2)
	pnt3 = arcpy.Point(x3,y3)
	pnt4 = arcpy.Point(x4,y4)
	array = arcpy.Array()
	array.add(pnt1)
	array.add(pnt2)
	array.add(pnt3)
	array.add(pnt4)
	array.add(pnt1)
	polygon = arcpy.Polygon(array)
	hullRectangles.append(polygon)
arcpy.CopyFeatures_management(hullRectangles, outputFeatureClass)
del updateRow, updateRows
