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
itemID = 'f25252e406c84662912cde5670c92fef'
url = "http://www.arcgis.com/sharing/rest/content/items/{0}/data".format(itemID)
layerData = makeRequest(url)
#for example of what json may look like returned see bottom of script
#print webmap

"""
Give field definition that omits one of the original fields (SUM_AREA) from Feature Service
"""
layer0 = layerData['layers'][0]
layer0['fields'] = [
        {
          "name" : "FID", 
          "type" : "esriFieldTypeInteger", 
          "actualType" : "int", 
          "alias" : "FID", 
          "sqlType" : "sqlTypeInteger", 
          "nullable" : "false", 
          "editable" : "false", 
          "domain" : "null", 
          "defaultValue" : "null"
        }, 
        {
          "name" : "DATE_", 
          "type" : "esriFieldTypeString", 
          "actualType" : "nvarchar", 
          "alias" : "DATE_", 
          "sqlType" : "sqlTypeNVarchar", "length" : 9, 
          "nullable" : "true", 
          "editable" : "true", 
          "domain" : "null", 
          "defaultValue" : "null"
        }, 
        {
          "name" : "NAME", 
          "type" : "esriFieldTypeString", 
          "actualType" : "nvarchar", 
          "alias" : "NAME", 
          "sqlType" : "sqlTypeNVarchar", "length" : 71, 
          "nullable" : "true", 
          "editable" : "true", 
          "domain" : "null", 
          "defaultValue" : "null"
        }
      ]

print layerData
text = json.dumps(layerData)

"""
Make request to update the item to have new renderer. Keep in mind you might have to change
more parameters to make it work depending on what else needs to change. This example
updates the field and the values in the renderer.
"""
"""
renderer = layerData['layers'][0]['layerDefinition']['drawingInfo']['renderer']
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
          'title': "TestUpdateMap3",
          'type': 'Web Map',
          'tags': 'remake'}
updateWebmap = makeRequest(url2, params)
print updateWebmap

"""
