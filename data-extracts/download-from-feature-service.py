# Script from "mike" at SoCalGIS.org
# https://socalgis.org/2018/03/28/extracting-more-features-from-map-services/

import arcpy
import urllib2
import json

# Setup
arcpy.env.overwriteOutput = True
baseURL = "https://www.gisonline.ms.gov/arcgis/rest/services/MDEQ/Viewer/MapServer/41"
fields = "*"
outdata = "D:/working_files/data.gdb/testdata"

# Get record extract limit
urlstring = baseURL + "?f=json"
j = urllib2.urlopen(urlstring)
js = json.load(j)
maxrc = int(js["maxRecordCount"])
print "Record extract limit: %s" % maxrc

# Get object ids of features
# "1=1" will return all features. Otherwise try something like "COUNTY='Monroe%20County'"
where = "1=1" 
urlstring = baseURL + "/query?where={}&returnIdsOnly=true&f=json".format(where)
j = urllib2.urlopen(urlstring)
js = json.load(j)
idfield = js["objectIdFieldName"]
idlist = js["objectIds"]
idlist.sort()
numrec = len(idlist)
print "Number of target records: %s" % numrec

# Gather features
print "Gathering records..."
fs = dict()
for i in range(0, numrec, maxrc):
  torec = i + (maxrc - 1)
  if torec > numrec:
    torec = numrec - 1
  fromid = idlist[i]
  toid = idlist[torec]
  where = "{} >= {} and {} <= {}".format(idfield, fromid, idfield, toid)
  print "  {}".format(where)
  urlstring = baseURL + "/query?where={}&returnGeometry=true&outFields={}&f=json".format(where,fields)
  fs[i] = arcpy.FeatureSet()
  fs[i].load(urlstring)

# Save features
print "Saving features..."
fslist = []
for key,value in fs.items():
  fslist.append(value)
arcpy.Merge_management(fslist, outdata)
print "Done!"