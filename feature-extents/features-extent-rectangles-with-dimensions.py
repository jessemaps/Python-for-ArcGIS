# Create extent rectangles for each feature, and write unique identifier, width, height, and orientation to attribute table.
# Source data should be in WGS84 so it uses degrees for the calculations. 
from arcpy import env

def DegreesToRadians(degrees):
	return degrees * (math.pi / 180)

# Update variables to match project data:
inputFeatureClass = "D:/working_files/data.gdb/Counties"
env.workspace = "D:/working_files/data.gdb"
outputFc = "Counties_for_DDP_WGS84_extentRects"

# The unique ID field plus new fields for WIDTH, HEIGHT, MID_LATITUDE, WIDTH_METERS, HEIGHT_METERS, and ORIENTATION are written to the new feature class.
# If you specify a template feature class, the template's fields will also be written out but the attributes will be empty.
outputFcTemplate = ""

#Update this field name to the name of the field in the input feature class that can uniquely identify each feature.
inputUniqueIdField = 'FIPS'

# Create new feature class to hold the output
arcpy.CreateFeatureclass_management(env.workspace, outputFc, "POLYGON", outputFcTemplate, "DISABLED", "DISABLED", inputFeatureClass)

outputWidthField = 'WIDTH'
outputHeightField = 'HEIGHT'
outputMidLatField = 'MID_LATITUDE'
outputWidthMetersField = 'WIDTH_METERS'
outputHeightMetersField = 'HEIGHT_METERS'
outputOrientationField = 'ORIENTATION'

arcpy.AddField_management(outputFc, inputUniqueIdField, "STRING", field_length="10")
arcpy.AddField_management(outputFc, outputWidthField, "DOUBLE")
arcpy.AddField_management(outputFc, outputHeightField, "DOUBLE")
arcpy.AddField_management(outputFc, outputMidLatField, "DOUBLE")
arcpy.AddField_management(outputFc, outputWidthMetersField, "DOUBLE")
arcpy.AddField_management(outputFc, outputHeightMetersField, "DOUBLE")
arcpy.AddField_management(outputFc, outputOrientationField, "STRING", field_length="10")

# outputValues stores the new polygons created from each input feature's extent
outputValues = []

# Get existing data with search cursor and make points at each corner and mid-point of the extent
with arcpy.da.SearchCursor(inputFeatureClass, ['SHAPE@', inputUniqueIdField]) as cursor:
	for row in cursor:
		shapeObj = row[0]
		
		extentRect = shapeObj.extent.polygon
		x1,y1,x2,y2,x3,y3,x4,y4 = [float(coord) for coord in shapeObj.extent.polygon.hullRectangle.split(" ")]
		width = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
		height = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)

		midpointLat = (shapeObj.extent.YMin + shapeObj.extent.YMax) / 2
		midpointLatRadians = DegreesToRadians(midpointLat);
		
		#Width and height formulas from: http://www.csgnetwork.com/degreelenllavcalc.html
		#Validated by: https://gis.stackexchange.com/questions/75528/understanding-terms-in-length-of-degree-formula/75535#75535
		#Constants
		m1 = 111132.92		# latitude calculation term 1
		m2 = -559.82		# latitude calculation term 2
		m3 = 1.175		# latitude calculation term 3
		m4 = -0.0023		# latitude calculation term 4
		p1 = 111412.84		# longitude calculation term 1
		p2 = -93.5		# longitude calculation term 2
		p3 = 0.118		# longitude calculation term 3

		# Calculate the length of a degree of latitude and longitude in meters
		OneDegLatMeters = m1 + (m2 * math.cos(2 * midpointLatRadians)) + (m3 * math.cos(4 * midpointLatRadians)) + (m4 * math.cos(6 * midpointLatRadians));
		OneDegLonMeters = (p1 * math.cos(midpointLatRadians)) + (p2 * math.cos(3 * midpointLatRadians)) + (p3 * math.cos(5 * midpointLatRadians));
		
		outputWidth = width * OneDegLonMeters
		outputHeight = height * OneDegLatMeters

		if outputWidth > outputHeight:
			orientation = 'Landscape'
		else:
			orientation = 'Portrait'
		
		outputValues.append((extentRect, row[1], width, height, midpointLat, outputWidth, outputHeight, orientation))

# Write new shapes with attributes with insert cursor
insertCursor = arcpy.da.InsertCursor(outputFc, ['SHAPE@', inputUniqueIdField, outputWidthField, outputHeightField, outputMidLatField, outputWidthMetersField, outputHeightMetersField, outputOrientationField])
for output in outputValues:
	insertCursor.insertRow(output)
del insertCursor
