# Adapted from Esri sample: https://desktop.arcgis.com/en/arcmap/latest/tools/conversion-toolbox/kml-to-layer.htm
# Description: Converts a directory of KMLs and copies the output into a single fGDB.
#              A 3 step process: first convert the KML files, then add a name attribute with the name of the source KML, and then copy the feature clases into a single GDB.

# Import system models
import arcpy, os

# Set workspace (where all the KMLs are)
arcpy.env.workspace="D:/Project_Folder/kml"

# Set local variables and location for the consolidated file geodatabase
outLocation = "D:/Project_Folder/kml_output"
MasterGDB = 'All_Imported_KML_Data.gdb'
MasterGDBLocation = os.path.join(outLocation, MasterGDB)

# Create the master FileGeodatabase
arcpy.CreateFileGDB_management(outLocation, MasterGDB)

# Convert all KMZ and KML files found in the current workspace
for kmz in arcpy.ListFiles('*.KM*'):
  print "CONVERTING: " + os.path.join(arcpy.env.workspace,kmz)
  arcpy.KMLToLayer_conversion(kmz, outLocation)


# Change the workspace to fGDB location
arcpy.env.workspace = outLocation

# Loop through all the FileGeodatabases within the workspace
wks = arcpy.ListWorkspaces('*', 'FileGDB')
# Skip the Master GDB
wks.remove(MasterGDBLocation)

for fgdb in wks:  
  # Set name of geodatabase
  KmlName = fgdb[fgdb.rfind(os.sep)+1:-4]
  #print "KmlName: " + KmlName
  
  # Change the workspace to the current FileGeodatabase
  arcpy.env.workspace = fgdb    

  # For every Featureclass inside, copy it to the Master and use the name from the original fGDB  
  featureClasses = arcpy.ListFeatureClasses('*', '', 'Placemarks')
  for fc in featureClasses:
    print "Adding KmlName field to " + fgdb + os.sep + 'Placemarks' + os.sep + fc
    arcpy.AddField_management(fgdb + os.sep + 'Placemarks' + os.sep + fc, "KmlName", "TEXT", field_length=10)
    arcpy.CalculateField_management(fgdb + os.sep + 'Placemarks' + os.sep + fc, "KmlName", '"' + KmlName + '"' ,"PYTHON")
    #print "COPYING: " + fc + " FROM: " + fgdb    
    fcCopy = fgdb + os.sep + 'Placemarks' + os.sep + fc    
    arcpy.FeatureClassToFeatureClass_conversion(fcCopy, MasterGDBLocation, KmlName + "_" + fc)
  

# Clean up
del kmz, wks, fc, featureClasses, fgdb
