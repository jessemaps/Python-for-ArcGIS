# Python-for-ArcGIS
Collection of random Python scripts I use in ArcGIS for various projects and want to use again

## data-driven-pages
Scripts used in conjunction with data-driven pages  

### ddp-focus-features-geometry-info.py
Write info to text file about each focus feature's geometry in the DDP series.
* map scale of feature's page in series
* focus feature width
* focus feature height
* focus feature area
* spatial reference name

## feature-extents
Work with the extents of each feature in a feature class.  

### feature-extent-halves.py
_**not yet implemented**_
Will create either North & South or East & West halves of each feature's extent rectangle depending on aspect ratio. 
Essentially this is so "tall" features get split into N-S halves and "wide" features get split into E-W halves.

### feature-extent-halves-N-S.py
Create North and South half extent rectangles for each feature.  
For each feature in a data set, output the north and south halves of the extent rectangle to a new feature class.  

### features-aspect-ratio.py
Write aspect ratio to new field in same feature class  
Taken from [GeoNet post by user csny490](https://community.esri.com/thread/92651)  
Demonstrates how to work with cursors and work with shapes of data and update attributes.  

### features-extent-rectangles.py
Create extent rectangles from input feature class.  
Extent rectangles are feature envelopes, oriented to North.  
These extent rectangles don't have attributes, so you have to later add the attributes by joining to the original data by object ID.  

### features-extent-rectangles-with-dimensions.py
Create extent rectangles for each feature, and write unique identifier, width, height, and orientation to attribute table.  
Extent rectangles are feature envelopes, oriented to North.  
*Input layer should be in WGS84.*
Width and height attributes are geodesic distances calculated in meters at the latitude of the center of each feature.  

### features-hull-rectangles.py
Create hull rectangles from input feature class.   
Adapted from [sample on GeoNet](https://community.esri.com/thread/92651) from user csny490  
Hull rectangles are different from envelopes in that they're rotated/oriented so longest side is parallel with widest section of shape.  
These Hull rectangles don't have attributes, so you have to later add the attributes by joining to the original data by object ID.  

## file-processing
Convert or consolidate files, usually in a batch.  

### Batch-KML-to-GDB.py
Combines multiple KML/KMZ files into 1 geodatabase. 
The Kml_to_Layer tool creates a new GDB for each KML file - this runs that tool on all KMLs in a folder, then copies them to a single GDB. 
It also adds a KmlName attribute to each new feature class with the source KML file name.  
This script adapted from the Esri sample: https://desktop.arcgis.com/en/arcmap/latest/tools/conversion-toolbox/kml-to-layer.htm  

