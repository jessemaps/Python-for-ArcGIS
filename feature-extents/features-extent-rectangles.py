# Create extent rectangles from input feature class. 
# Extent rectangles are feature envelopes, oriented to North.
# These extent rectangles don't have attributes, so you have to later add the attributes by joining to the original data by object ID.
from arcpy import env

# Update variables to match project data:
featureClass = "D:/working_files/data.gdb/Counties"
env.workspace = "D:/working_files/data.gdb"
outputFeatureClass = "County_ExtentRectangles"

extentRectangles = []
updateRows = arcpy.da.UpdateCursor(featureClass, ["SHAPE@","ASP_RATIO"])
for updateRow in updateRows:
	shapeObj = updateRow[0]
	extentRect = shapeObj.extent.polygon
	extentRectangles.append(extentRect)
arcpy.CopyFeatures_management(extentRectangles, outputFeatureClass)
del updateRow, updateRows
