#Export PDF files with page Names from a specific attribute instead of the DDP page ID in the output file names.
mxd = arcpy.mapping.MapDocument("CURRENT")
for pageNum in range(1,mxd.dataDrivenPages.pageCount+1):
	mxd.dataDrivenPages.currentPageID = pageNum
	#STATE_NAME is the field name containing the page names - update as necessary
	pageName = mxd.dataDrivenPages.pageRow.STATE_NAME
	#Edit output path to your own project folder:
	arcpy.mapping.ExportToPDF(mxd,r"C:\temp\GIS_Files\CD_" + pageName + ".pdf","PAGE_LAYOUT",1,1,1152,"BEST","CMYK",True,"LZW","VECTORIZE_BITMAP",True,True,"LAYERS_ONLY",False,80)
del mxd