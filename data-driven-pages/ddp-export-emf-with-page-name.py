#Export EMF files with page Names from a specific attribute instead of the DDP page ID in the output file names.
mxd = arcpy.mapping.MapDocument("CURRENT")
for pageNum in range(1,mxd.dataDrivenPages.pageCount+1):
	mxd.dataDrivenPages.currentPageID = pageNum
	#STATE_ABBR is the field name containing the page names - update as necessary
	pageName = mxd.dataDrivenPages.pageRow.STATE_ABBR
	pageDescription = mxd.dataDrivenPages.pageRow.STATE_NAME + " outline map"
  #Edit output path to your own project folder:
	arcpy.mapping.ExportToEMF(mxd,r"C:\temp\GIS_Files\State_" + pageName + ".emf","PAGE_LAYOUT",1,1,1152,"BEST",pageDescription,"VECTORIZE_BITMAP",True)
del mxd