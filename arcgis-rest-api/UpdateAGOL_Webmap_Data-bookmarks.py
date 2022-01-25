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
itemID = '1742ad32f49141d09c99408c0b3692e2'
#webmapUrl = "http://www.arcgis.com/sharing/rest/content/items/{0}".format(itemID)
#webmap = makeRequest(webmapUrl)
webmapDataUrl = "http://www.arcgis.com/sharing/rest/content/items/{0}/data".format(itemID)
webmapData = makeRequest(webmapDataUrl)


#bookmarks = webmapData['bookmarks']
#print json.dumps(bookmarks, indent=2, sort_keys=False)
webmapData['bookmarks'] = [
  {
    "name": "Europe 1944", 
    "extent": {
      "xmin": -1361272.1638402133, 
      "ymin": 4333545.722728822, 
      "ymax": 8486828.091631055, 
      "xmax": 4059030.3859167644, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "Atlantic Wall", 
    "extent": {
      "xmin": -7752630.720931811, 
      "ymin": 2308270.221285331, 
      "ymax": 16005785.689985273, 
      "xmax": 11482594.572971107, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "Calais", 
    "extent": {
      "xmin": 17304.163941496416, 
      "ymin": 6544223.677811424, 
      "ymax": 6757941.608896674, 
      "xmax": 324275.26953461627, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "D-Day Invasion-Region", 
    "extent": {
      "xmin": -692295.2922885282, 
      "ymin": 6119114.703470066, 
      "ymax": 6829673.318408875, 
      "xmax": 600407.730070029, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "D-Day Invasion-Local", 
    "extent": {
      "xmin": -377068.98764050426, 
      "ymin": 6289722.150602436, 
      "ymax": 6645001.458071917, 
      "xmax": 269282.52353891404, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "D-Day Invasion-Landing", 
    "extent": {
      "xmin": -221748.94616498513, 
      "ymin": 6261593.324193512, 
      "ymax": 6481731.965654713, 
      "xmax": 81553.18207044795, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }, 
  {
    "name": "After D-Day", 
    "extent": {
      "xmin": -801141.6205665902, 
      "ymin": 5128490.816894444, 
      "ymax": 6823558.356146062, 
      "xmax": 1779372.454340274, 
      "spatialReference": {
        "wkid": 102100, 
        "latestWkid": 3857
      }
    }
  }
]

#print 'Updated bookmarks: '
#print json.dumps(bookmarks, indent=2, sort_keys=False)
text = json.dumps(webmapData)
#formattedText = json.dumps(webmapData, indent=2, sort_keys=False)
#print formattedText

print 'performing update...'
updateUrl = "http://www.arcgis.com/sharing/rest/content/users/{0}/items/{1}/update".format(username,itemID)
print 'updateUrl: ' + updateUrl
params = {'token': token,
          'f': 'json',
          'text': text}
updateWebmap = makeRequest(updateUrl, params)
print updateWebmap
print 'update complete.'
#print json.dumps(updateWebmap, indent=2, sort_keys=False)


