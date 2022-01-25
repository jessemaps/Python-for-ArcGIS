#Export to PNG files with page Names from a specific attribute instead of the DDP page ID in the output file names.
mxd = arcpy.mapping.MapDocument("CURRENT")
for pageNum in range(1,mxd.dataDrivenPages.pageCount+1):
	mxd.dataDrivenPages.currentPageID = pageNum
	#STATE_ABBR is the field name containing the page names - update as necessary
	pageName = mxd.dataDrivenPages.pageRow.STATE_ABBR
	pageDescription = mxd.dataDrivenPages.pageRow.STATE_NAME + " outline map"
  #Edit output path to your own project folder:
	arcpy.mapping.ExportToPNG(mxd,r"C:\temp\GIS_Files\state_" + pageName + ".png","PAGE_LAYOUT",1,1,96,False,"24-BIT_TRUE_COLOR","255, 255, 255","255, 255, 255",False)
del mxd
