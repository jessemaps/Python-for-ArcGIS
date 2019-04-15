# Create North and South half extent rectangles for each feature.
# For each feature in a data set, output the north and south halves of the extent rectangle to a new feature class.
from arcpy import env

# Update variables to match project data:
inputFeatureClass = "D:/working_files/data.gdb/Counties"
env.workspace = "D:/working_files/data.gdb"
inputUniqueIdField = 'FIPS'
outputFc = "ExtentRectangle_halves"
outputFcTemplate = "OutputTemplate"
outputPartIdentifierField = 'Page_Part'

# outputValues stores the new polygons created from each input feature's extent
outputValues = []

# Create new feature class to hold the output
arcpy.CreateFeatureclass_management(env.workspace, outputFc, "POLYGON", outputFcTemplate, "DISABLED", "DISABLED", inputFeatureClass)

# Get existing data with search cursor and make points at each corner and mid-point of the extent
with arcpy.da.SearchCursor(inputFeatureClass, ['SHAPE@', inputUniqueIdField]) as cursor:
	for row in cursor:
		shapeObj = row[0]
		extentRect = shapeObj.extent.polygon
		# 1  2
		# 3  4
		# 5  6
		YAvg = ((shapeObj.extent.YMax + shapeObj.extent.YMin)/2)
		pnt1 = arcpy.Point(shapeObj.extent.XMin, shapeObj.extent.YMax)
		pnt2 = arcpy.Point(shapeObj.extent.XMax, shapeObj.extent.YMax)
		pnt3 = arcpy.Point(shapeObj.extent.XMin, YAvg)
		pnt4 = arcpy.Point(shapeObj.extent.XMax, YAvg)
		pnt5 = arcpy.Point(shapeObj.extent.XMin,shapeObj.extent.YMin)
		pnt6 = arcpy.Point(shapeObj.extent.XMax,shapeObj.extent.YMin)

		topArray = arcpy.Array()
		topArray.add(pnt1)
		topArray.add(pnt2)
		topArray.add(pnt4)
		topArray.add(pnt3)
		topArray.add(pnt1)
		topPolygon = arcpy.Polygon(topArray)
		outputValues.append((topPolygon, row[1], 'north'))

		bottomArray = arcpy.Array()
		bottomArray.add(pnt3)
		bottomArray.add(pnt4)
		bottomArray.add(pnt6)
		bottomArray.add(pnt5)
		bottomArray.add(pnt3)
		bottomPolygon = arcpy.Polygon(bottomArray)
		outputValues.append((bottomPolygon, row[1], 'south'))

# Write new shapes with attributes with insert cursor
insertCursor = arcpy.da.InsertCursor(outputFc, ['SHAPE@', inputUniqueIdField, outputPartIdentifierField])
for output in outputValues:
	insertCursor.insertRow(output)
del insertCursor
