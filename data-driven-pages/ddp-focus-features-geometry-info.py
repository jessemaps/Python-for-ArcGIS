# Write info to text file about each focus feature's geometry in the DDP series.

# Output text file with path:
outputTextFile = r"D:\working_files\Project_Folder\DDP_feature_properties.txt"

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
for pageNum in range(1,mxd.dataDrivenPages.pageCount+1):
	mxd.dataDrivenPages.currentPageID = pageNum
	#UniqueNameField is the field name containing the page names - update to match project data:
	pageName = mxd.dataDrivenPages.pageRow.UniqueNameField
	pageShape = mxd.dataDrivenPages.pageRow.SHAPE
	dataFrameExtent = df.extent
	dfWidth = dataFrameExtent.XMax - dataFrameExtent.XMin
	dataFrameExtent.XMin  -> dataFrameExtent.XMin + dfWidth * 0.0435
	extent = pageShape.extent
	width = extent.XMax - extent.XMin
	height = extent.YMax - extent.YMin
	with open(outputTextFile, "a") as f:
		f.write(pageName + "\t" + str(df.scale) + "\t" + str(width) + "\t" + str(height) + "\t" + str(pageShape.area) + "\t" + pageShape.spatialReference.name + "\n")
del mxd
