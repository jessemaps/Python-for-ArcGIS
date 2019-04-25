# Create North and South half extent rectangles for each feature.
# For each feature in a data set, output the north and south halves of the extent rectangle to a new feature class.
from arcpy import env

# Update variables to match project data:
inputFeatureClass = "D:/working_files/data.gdb/Counties"
env.workspace = "D:/working_files/data.gdb"
inputUniqueIdField = 'FIPS'
outputFc = "ExtentRectangle_halves"
# The output feature class' template must at least include fields for:
#  - unique ID from the input features in the same data type as input unique ID
#  - string field that will hold the name of the new secondary identifier of the shape - either 'North', 'South', 'East', or 'West'
# Only these 2 fields are written to the new feature class
outputFcTemplate = "OutputTemplate"
outputSecondaryIdentifierField = 'Page_Part'
# Aspect ratio at which portrait-oriented shapes will be split vertically
aspectRatioBreakpoint = 1

# outputValues stores the new polygons created from each input feature's extent
outputValues = []

# Create new feature class to hold the output
arcpy.CreateFeatureclass_management(env.workspace, outputFc, "POLYGON", outputFcTemplate, "DISABLED", "DISABLED", inputFeatureClass)

# Function to create polygon from input points
def CreateFourPointPolygon(pt1, pt2, pt3, pt4):
	pointArray = arcpy.Array()
	pointArray.add(pt1)
	pointArray.add(pt2)
	pointArray.add(pt3)
	pointArray.add(pt4)
	pointArray.add(pt1)
	polygon = arcpy.Polygon(pointArray)
	return polygon

# Get existing data with search cursor and make points at each corner and mid-point of the extent
with arcpy.da.SearchCursor(inputFeatureClass, ['SHAPE@', inputUniqueIdField]) as cursor:
	for row in cursor:
		shapeObj = row[0]
		extentRect = shapeObj.extent.polygon
		
		width = shapeObj.extent.XMax - shapeObj.extent.XMin
		height = shapeObj.extent.YMax - shapeObj.extent.YMin
		aspectRatio = width/height
		if height > width:
			aspectRatio = height / width
		
		# 1  2  3
		# 4  5  6
		# 7  8  9
		YAvg = ((shapeObj.extent.YMax + shapeObj.extent.YMin)/2)
		XAvg = ((shapeObj.extent.XMax + shapeObj.extent.XMin)/2)
		pnt1 = arcpy.Point(shapeObj.extent.XMin, shapeObj.extent.YMax)
		pnt2 = arcpy.Point(XAvg, shapeObj.extent.YMax)
		pnt3 = arcpy.Point(shapeObj.extent.XMax, shapeObj.extent.YMax)
		pnt4 = arcpy.Point(shapeObj.extent.XMin, YAvg)
		pnt5 = arcpy.Point(XAvg, YAvg)
		pnt6 = arcpy.Point(shapeObj.extent.XMax, YAvg)
		pnt7 = arcpy.Point(shapeObj.extent.XMin, shapeObj.extent.YMin)
		pnt8 = arcpy.Point(XAvg, shapeObj.extent.YMin)
		pnt9 = arcpy.Point(shapeObj.extent.XMax, shapeObj.extent.YMin)
		
		if height > width:
			# Portrait orientation - split into North and South areas
			topPolygon = CreateFourPointPolygon(pnt1, pnt3, pnt6, pnt4)
			outputValues.append((topPolygon, row[1], 'North'))
			bottomPolygon = CreateFourPointPolygon(pnt4, pnt6, pnt9, pnt7)
			outputValues.append((bottomPolygon, row[1], 'South'))
		else:
			# Landscape - split into East and  West
			westPolygon = CreateFourPointPolygon(pnt1, pnt2, pnt8, pnt7)
			outputValues.append((westPolygon, row[1], 'West'))
			eastPolygon = CreateFourPointPolygon(pnt2, pnt3, pnt9, pnt8)
			outputValues.append((eastPolygon, row[1], 'East'))

# Write new shapes with attributes with insert cursor
insertCursor = arcpy.da.InsertCursor(outputFc, ['SHAPE@', inputUniqueIdField, outputSecondaryIdentifierField])
for output in outputValues:
	insertCursor.insertRow(output)
del insertCursor
