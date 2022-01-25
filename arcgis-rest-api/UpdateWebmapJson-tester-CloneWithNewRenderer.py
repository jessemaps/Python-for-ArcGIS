# Modules needed
import urllib, urllib2, httplib
import json
import socket
import os, sys, time
from time import localtime, strftime


"""
Variable Setup: These are the Admin variables used in this script. Changes
should be made to username and password that reflect an ADMIN user found within
the organization.
"""
# Admin Variables to be changed.
username = ""
password = ""
# portalName - include Web Adaptor name if it has one or use arcgis.com for AGOL
# organizational account.
portalName = 'http://arcgis.com'

# Host name will be generated based on the computer name. No Changes need to be
# made.
hostname = "Http://" + socket.getfqdn()


"""
Setup of Monkey Patch, Token, Logs, and Service Requests.
"""
# Monkey Patch httplib read
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)


# Generate Token
if "arcgis.com" in portalName:
    token_URL = 'https://www.arcgis.com/sharing/generateToken'
else:
    token_URL = "{0}/sharing/generateToken".format(portalName)
token_params = {'username':username,'password': password,'referer': hostname,'f':'json'}
token_request = urllib2.Request(token_URL, urllib.urlencode(token_params))
token_response = urllib2.urlopen(token_request)
token_string = token_response.read()
token_obj = json.loads(token_string)
token = token_obj['token']

# Define basic http request
def makeRequest(URL, PARAMS={'f': 'json','token': token}):
    global hostname
    request = urllib2.Request(URL, urllib.urlencode(PARAMS))
    request.add_header('Referer', hostname)
    response = urllib2.urlopen(request).read()
    JSON = json.loads(response)
    return JSON


"""
Make request to pull json for webmap. Item data request will show the json for
the webmap. Make sure it is public to run this:
http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Item_Data/02r300000075000000/
"""
itemID = '14571e9c93b7410eaa32e33010bdb18f'
url = "http://www.arcgis.com/sharing/rest/content/items/{0}/data".format(itemID)
webmap = makeRequest(url)
#for example of what json may look like returned see bottom of script
print webmap

"""
Make request to update the item to have new renderer. Keep in mind you might have to change
more parameters to make it work depending on what else needs to change. This example
updates the field and the values in the renderer.
"""

renderer = webmap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']
#[0] is for first layer in map, so this must be done for each layer.

renderer['field1'] = 'Test12'
#uniqueValueInfos - dictionary in webmap which defines how symbology will look
renderer['uniqueValueInfos'] = [{ 
          "value": "blue",
          "symbol": {
            "color": [
              252,
              225,
              56,
              128
            ],
            "size": 6,
            "angle": 0,
            "xoffset": 0,
            "yoffset": 0,
            "type": "esriSMS",
            "style": "esriSMSCircle",
            "outline": {
              "color": [
                0,
                0,
                128,
                255
              ],
              "width": 0,
              "type": "esriSLS",
              "style": "esriSLSSolid"
            }
          },
          "label": "Blue",
          "description": 'Blue'
        },
        {
          "value": "Yellow",
          "symbol": {
            "color": [
              255,
              247,
              153,
              128
            ],
            "size": 6,
            "angle": 0,
            "xoffset": 0,
            "yoffset": 0,
            "type": "esriSMS",
            "style": "esriSMSCircle",
            "outline": {
              "color": [
                0,
                0,
                128,
                255
              ],
              "width": 0,
              "type": "esriSLS",
              "style": "esriSLSSolid"
            }
          },
          "label": "Yellow",
          "description": 'Yellow'
        }
      ]

print webmap
text = json.dumps(webmap)
url2 = "http://www.arcgis.com/sharing/rest/content/users/{0}/addItem".format(username)
params = {'token': token,
          'f': 'json',
          'text': text,
          'title': "TestUpdateMap4",
          'type': 'Web Map',
          'tags': 'remake'}
updateWebmap = makeRequest(url2, params)
print updateWebmap

raw_input()
"""example json from webmap:
    {
  "operationalLayers": [{
    "id": "ZeroPointsNAD_296",
    "layerType": "ArcGISFeatureLayer",
    "url": "http://services.arcgis.com/Wl7Y1m92PbjtJs5n/arcgis/rest/services/ZeroPointsNAD/FeatureServer/0",
    "visibility": true,
    "opacity": 1,
    "title": "ZeroPointsNAD",
    "itemId": "dc244e9f44234b21892b94b4f7d136c0",
    "layerDefinition": {"drawingInfo": {"renderer": {
      "type": "uniqueValue",
      "field1": "Test12",
      "uniqueValueInfos": [{
        "value": "test",
        "symbol": {
          "color": [
            252,
            225,
            56,
            128
          ],
          "size": 6,
          "angle": 0,
          "xoffset": 0,
          "yoffset": 0,
          "type": "esriSMS",
          "style": "esriSMSCircle",
          "outline": {
            "color": [
              0,
              0,
              128,
              255
            ],
            "width": 0,
            "type": "esriSLS",
            "style": "esriSLSSolid"
          }
        },
        "label": "test",
        "description": null
      }]
    }}},
    "popupInfo": {
      "title": "ZeroPointsNAD: {Test12}",
      "fieldInfos": [
        {
          "fieldName": "OBJECTID",
          "label": "OBJECTID",
          "isEditable": false,
          "tooltip": "",
          "visible": false,
          "format": null,
          "stringFieldOption": "textbox"
        },
        {
          "fieldName": "Test12",
          "label": "Test12",
          "isEditable": true,
          "tooltip": "",
          "visible": true,
          "format": null,
          "stringFieldOption": "textbox"
        },
        {
          "fieldName": "GlobalID",
          "label": "",
          "isEditable": false,
          "tooltip": "",
          "visible": false,
          "format": null,
          "stringFieldOption": "textbox"
        }
      ],
      "description": null,
      "showAttachments": true,
      "mediaInfos": []
    }
  }],
  "baseMap": {
    "baseMapLayers": [{
      "id": "defaultBasemap",
      "layerType": "ArcGISTiledMapServiceLayer",
      "opacity": 1,
      "visibility": true,
      "url": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer"
    }],
    "title": "Topographic"
  },
  "spatialReference": {
    "wkid": 102100,
    "latestWkid": 3857
  },
  "version": "2.0",
  "applicationProperties": {"viewing": {
    "routing": {"enabled": true},
    "basemapGallery": {"enabled": true},
    "measure": {"enabled": true}
  }}
}
"""