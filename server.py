#!/usr/bin/env python
"""Web server for the Trendy Lights application.

The overall architecture looks like:

               server.py         script.js
 ______       ____________       _________
|      |     |            |     |         |
|  EE  | <-> | App Engine | <-> | Browser |
|______|     |____________|     |_________|
     \                               /
      '- - - - - - - - - - - - - - -'

The code in this file runs on App Engine. It's called when the user loads the
web page and when details about a polygon are requested.

Our App Engine code does most of the communication with EE. It uses the
EE Python library and the service account specified in config.py. The
exception is that when the browser loads map tiles it talks directly with EE.

The basic flows are:

1. Initial page load

When the user first loads the application in their browser, their request is
routed to the get() function in the MainHandler class by the framework we're
using, webapp2.

The get() function sends back the main web page (from index.html) along
with information the browser needs to render an Earth Engine map and
the IDs of the polygons to show on the map. This information is injected
into the index.html template through a templating engine called Jinja2,
which puts information from the Python context into the HTML for the user's
browser to receive.

Note: The polygon IDs are determined by looking at the static/polygons
folder. To add support for another polygon, just add another GeoJSON file to
that folder.

2. Getting details about a polygon

When the user clicks on a polygon, our JavaScript code (in static/script.js)
running in their browser sends a request to our backend. webapp2 routes this
request to the get() method in the DetailsHandler.

This method checks to see if the details for this polygon are cached. If
yes, it returns them right away. If no, we generate a Wikipedia URL and use
Earth Engine to compute the brightness trend for the region. We then store
these results in a cache and return the result.

Note: The brightness trend is a list of points for the chart drawn by the
Google Visualization API in a time series e.g. [[x1, y1], [x2, y2], ...].

Note: memcache, the cache we are using, is a service provided by App Engine
that temporarily stores small values in memory. Using it allows us to avoid
needlessly requesting the same data from Earth Engine over and over again,
which in turn helps us avoid exceeding our quota and respond to user
requests more quickly.

"""

import json
import os

import config
import config
import ee
import ee
import jinja2
import webapp2

from google.appengine.api import memcache

cloudiness = None

###############################################################################
#                             Web request handlers.                           #
###############################################################################


class MainHandler(webapp2.RequestHandler):
  """A servlet to handle requests to load the main Trendy Lights web page."""

  def get(self, path=''):
    """Returns the main web page, populated with EE map and polygon info."""
    mapid_2000 = GetTrendyMapId_2000()
    mapid_2001 = GetTrendyMapId_2001()
    mapid_2002 = GetTrendyMapId_2002()
    mapid_2003 = GetTrendyMapId_2003()
    mapid_2004 = GetTrendyMapId_2004()
    mapid_2005 = GetTrendyMapId_2005()
    mapid_2006 = GetTrendyMapId_2006()
    mapid_2007 = GetTrendyMapId_2007()
    mapid_2008 = GetTrendyMapId_2008()
    mapid_2009 = GetTrendyMapId_2009()
    mapid_2010 = GetTrendyMapId_2010()
    mapid_2011 = GetTrendyMapId_2011()
    mapid_2012 = GetTrendyMapId_2012()
    mapid_2013 = GetTrendyMapId_2013()
    mapid_2014 = GetTrendyMapId_2014()
    #mapid_2015 = GetTrendyMapId_2015()
    #mapid_2016 = GetTrendyMapId_2016()
    template_values = {
        'eeMapId_2000': mapid_2000['mapid'],
        'eeToken_2000': mapid_2000['token'],
        'eeMapId_2001': mapid_2001['mapid'],
        'eeToken_2001': mapid_2001['token'],
        'eeMapId_2002': mapid_2002['mapid'],
        'eeToken_2002': mapid_2002['token'],
        'eeMapId_2003': mapid_2003['mapid'],
        'eeToken_2003': mapid_2003['token'],
        'eeMapId_2004': mapid_2004['mapid'],
        'eeToken_2004': mapid_2004['token'],
        'eeMapId_2005': mapid_2005['mapid'],
        'eeToken_2005': mapid_2005['token'],
        'eeMapId_2006': mapid_2006['mapid'],
        'eeToken_2006': mapid_2006['token'],
        'eeMapId_2007': mapid_2007['mapid'],
        'eeToken_2007': mapid_2007['token'],
        'eeMapId_2008': mapid_2008['mapid'],
        'eeToken_2008': mapid_2008['token'],
        'eeMapId_2009': mapid_2009['mapid'],
        'eeToken_2009': mapid_2009['token'],
        'eeMapId_2010': mapid_2010['mapid'],
        'eeToken_2010': mapid_2010['token'],
        'eeMapId_2011': mapid_2011['mapid'],
        'eeToken_2011': mapid_2011['token'],
        'eeMapId_2012': mapid_2012['mapid'],
        'eeToken_2012': mapid_2012['token'],
        'eeMapId_2013': mapid_2013['mapid'],
        'eeToken_2013': mapid_2013['token'],
        'eeMapId_2014': mapid_2014['mapid'],
        'eeToken_2014': mapid_2014['token'],
        #'eeMapId_2015': mapid_2015['mapid'],
        #'eeToken_2015': mapid_2015['token'],
        #'eeMapId_2016': mapid_2016['mapid'],
        #'eeToken_2016': mapid_2016['token'],
        'serializedPolygonIds': json.dumps(POLYGON_IDS)
    }
    template = JINJA2_ENVIRONMENT.get_template('index.html')
    self.response.out.write(template.render(template_values))


class DetailsHandler(webapp2.RequestHandler):
  """A servlet to handle requests for details about a Polygon."""

  def get(self):
    """Returns details about a polygon."""
    polygon_id = self.request.get('polygon_id')
    if polygon_id in POLYGON_IDS:
      content = GetPolygonTimeSeries(polygon_id)
    else:
      content = json.dumps({'error': 'Unrecognized polygon ID: ' + polygon_id})
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(content)


# Define webapp2 routing from URL paths to web request handlers. See:
# http://webapp-improved.appspot.com/tutorials/quickstart.html
app = webapp2.WSGIApplication([
    ('/details', DetailsHandler),
    ('/', MainHandler),
])


###############################################################################
#                                   Helpers.                                  #
###############################################################################

def cloudBand(image):
    clouds = ee.Algorithms.Landsat.simpleCloudScore(image).select('cloud');
    return image.addBands(clouds.lte(40))

def cloudBandF(image):
    return cloudBand(image)

# Add these two lines for each year below. Beware of leftField differences, see 2004	
#innerJoin = ee.Join.inner();
#filterTimeEq = ee.Filter.equals({leftField: 'system:time_start', rightField: 'system:time_start'});

def MergeBands(element):
    return ee.Image.cat(element.get('primary'), element.get('secondary'))

def ndviAdd(image):
    ndvi = ee.Image(image).normalizedDifference(['B5', 'B4']).select([0], ['NDVI']);
    return ee.Image(image).addBands(ndvi)	

def cloudMask(image):
    clouds = ee.Image(image).select('cloud');
    mask = ee.Image(image).mask().And(clouds);
    return ee.Image(image).mask(mask)

def cloudMaskF(image):
    return cloudMask(ee.Image(image))	

def unmaski(image):
    return image.unmask()	
	
def GetTrendyMapId_2000():

	start_date = '2000-01-01';
	end_date = '2000-12-31';
	llanos = ee.FeatureCollection('ft:1X_CeRfYiZ_4F-G9cu78pxjKTI_xD6yHeFiLvVOki');
	
	toaL7 = ee.ImageCollection('LANDSAT/LE7_L1T_TOA').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 58))));
	toaL5 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 58))));
	srL7 = ee.ImageCollection('LEDAPS/LE7_L1T_SR').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 58))));
	srL5 = ee.ImageCollection('LEDAPS/LT5_L1T_SR').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 58))));
	
	cloudTOAL7 = toaL7.map(cloudBandF);
	cloudTOAL5 = toaL5.map(cloudBandF);
	
	innerJoinedL7 = ee.Join.inner().apply(cloudTOAL7.select('cloud'), srL7, ee.Filter.equals(leftField = 'system:time_start', rightField = 'system:time_start')).map(MergeBands).map(ndviAdd);
	innerJoinedL5 = ee.Join.inner().apply(cloudTOAL5.select('cloud'), srL5, ee.Filter.equals(leftField = 'system:time_start', rightField = 'system:time_start')).map(MergeBands).map(ndviAdd);
	
	maskedColl7 = innerJoinedL7.map(cloudMaskF);
	maskedColl5 = innerJoinedL5.map(cloudMaskF);

	maxValueComposite7 = ee.ImageCollection(maskedColl7).qualityMosaic('NDVI');
	maxValueComposite5 = ee.ImageCollection(maskedColl5).qualityMosaic('NDVI');
	maxValueComposite = ee.ImageCollection.fromImages([maxValueComposite5, maxValueComposite7]).mosaic();
	
	llanos7 = ee.ImageCollection(maskedColl7).filter(ee.Filter.Or(ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70040562000023EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70040572000023EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70050552000046EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70050562000110AGS01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060552000005EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060562000005EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060572000005EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070562000348EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070572000076EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070582000348EDC00')));
	llanos5 = ee.ImageCollection(maskedColl5).filter(ee.Filter.Or(ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50050572000278XXX02'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50060582000029XXX02')));
	
	joinedICs = ee.ImageCollection(llanos5.merge(llanos7));
	mosaico = joinedICs.map(unmaski).mosaic();
	nmosaico = mosaico.where(mosaico.eq(0), maxValueComposite);

	return nmosaico.getMapId(vizParams_L5L7)

def GetTrendyMapId_2001():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562001009AGS00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572001033XXX01');
    image3 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050552001008AAA02');
    image4 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050562001008AAA02');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572001008AAA02');
    image6 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060552001031XXX01');
    image7 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060562001047XXX01');
    image8 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060572001047XXX01');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582001031XXX01');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562001030AGS00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572001062EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582001062EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2002():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562002332EDC00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572002004CUB00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552002051AGS00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562002003EDC00');
    image5 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050572002003EDC00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552002026AGS00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562002026AGS00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572002362AGS01');
    image9 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060582002362AGS01');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562002017EDC01');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572002017EDC01');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582002273EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2003():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562003031PFS00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572003359CUB00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552003006PFS00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562003022PFS00');
    image5 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050572003022PFS00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552003045AGS00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562003013EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572003045EDC01');
    image9 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060582003013PFS00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562003004AGS00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572003004AGS00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582003004AGS00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2004():

	start_date = '2004-01-01';
	end_date = '2004-12-31';
	llanos = ee.FeatureCollection('ft:1X_CeRfYiZ_4F-G9cu78pxjKTI_xD6yHeFiLvVOki');
	
	toaL7 = ee.ImageCollection('LANDSAT/LE7_L1T_TOA').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 58))));
	toaL5 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 58))));
	srL7 = ee.ImageCollection('LEDAPS/LE7_L1T_SR').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 55)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 7), ee.Filter.eq('WRS_ROW', 58))));
	srL5 = ee.ImageCollection('LEDAPS/LT5_L1T_SR').filterDate(start_date, end_date).filterBounds(llanos).filter(ee.Filter.Or(ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 56)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 4), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 5), ee.Filter.eq('WRS_ROW', 57)), ee.Filter.And(ee.Filter.eq('WRS_PATH', 6), ee.Filter.eq('WRS_ROW', 58))));
	
	cloudTOAL7 = toaL7.map(cloudBandF);
	cloudTOAL5 = toaL5.map(cloudBandF);
	
	#innerJoinedL7 = innerJoin.apply(cloudTOAL7.select('cloud'), srL7, filterTimeEq).map(MergeBands).map(ndviAdd);
	# Note la diferencia en leftField = sin corchete, con respecto a la version de JavaScript
	innerJoinedL7 = ee.Join.inner().apply(cloudTOAL7.select('cloud'), srL7, ee.Filter.equals(leftField = 'system:time_start', rightField = 'system:time_start')).map(MergeBands).map(ndviAdd);
	innerJoinedL5 = ee.Join.inner().apply(cloudTOAL5.select('cloud'), srL5, ee.Filter.equals(leftField = 'system:time_start', rightField = 'system:time_start')).map(MergeBands).map(ndviAdd);
	
	maskedColl7 = innerJoinedL7.map(cloudMaskF);
	maskedColl5 = innerJoinedL5.map(cloudMaskF);

	maxValueComposite7 = ee.ImageCollection(maskedColl7).qualityMosaic('NDVI');
	maxValueComposite5 = ee.ImageCollection(maskedColl5).qualityMosaic('NDVI');
	maxValueComposite = ee.ImageCollection.fromImages([maxValueComposite5, maxValueComposite7]).mosaic();
	
	llanos7 = ee.ImageCollection(maskedColl7).filter(ee.Filter.Or(ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70050552004041EDC01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70050562004041EDC01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060552004032EDC01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060562004032EDC01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70060572004032EDC01'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070562004359EDC00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070572004039EDC02'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LE70070582004023ASN01')));
	llanos5 = ee.ImageCollection(maskedColl5).filter(ee.Filter.Or(ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50040562004026CUB00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50040572004026CUB00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50050572004033CUB00'), ee.Filter.eq('LANDSAT_SCENE_ID', 'LT50060582004040CUB00')));
	
	joinedICs = ee.ImageCollection(llanos5.merge(llanos7));
	mosaico = joinedICs.map(unmaski).mosaic();
	nmosaico = mosaico.where(mosaico.eq(0), maxValueComposite);

	return nmosaico.getMapId(vizParams_L5L7)

def GetTrendyMapId_2005():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562005012CUB01');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572005012CUB01');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552005059ASN00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562005363EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572005307CUB00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552005114EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562005194ASN00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572005194ASN00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582005026CUB01');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562005073EDC00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572005073EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582005073EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)
    
def GetTrendyMapId_2006():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562006351CUB00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572006335CUB00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552006062EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562006142EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572006038CUB00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552006037EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562006037EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572006101ASN00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582006045CUB00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562006140EDC00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572006140EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582006044ASN00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)
    
def GetTrendyMapId_2007():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562007050CUB01');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572007050CUB01');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552007033EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562007049EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572007009CUB00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552007024EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562007344EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572007344EDC00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582007016CUB00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562007031EDC00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572007031EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582007047EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2008():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562008021CUB00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572008021CUB00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552008020EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562008020EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572008028CUB00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552008107EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562008363EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572008027EDC00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582008099CUB00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562008002EDC00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572008018EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582008002EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2009():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562009311CUB00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572009311CUB00');
    image3 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050552009334CHM01');
    image4 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050562009334CHM01');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572009094CUB00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552009013EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562009205ASN00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572009365EDC01');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582009069CUB00');
    image10 = ee.Image('LEDAPS/LT5_L1T_SR/LT50070562009348CHM00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572009052EDC00');
    image12 = ee.Image('LEDAPS/LT5_L1T_SR/LT50070582009252CHM00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2010():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562010042CHM00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572010042CUB01');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552010009EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562010009EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572010017CUB00');
    image6 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060552010056CHM00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562010048ASN00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572010112EDC00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582010024CUB00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562010343EDC00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572010023EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582010023EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2011():

    image1 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040562011013CUB00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572011013CUB00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552011044EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562011012EDC00');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572011036CUB00');
    image6 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060552011091CHM00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562011019EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572011019EDC00');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582011219CUB00');
    image10 = ee.Image('LEDAPS/LT5_L1T_SR/LT50070562011098CHM00');
    image11 = ee.Image('LEDAPS/LT5_L1T_SR/LT50070572011114CHM00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582011074EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

def GetTrendyMapId_2012():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562012008EDC00');
    image2 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040572012264ASN00');
    image3 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050552012047EDC00');
    image4 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050562012047EDC00');
    image5 = ee.Image('LEDAPS/LE7_L1T_SR/LE70050572012351EDC00');
    image6 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060552012022EDC00');
    image7 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060562012022EDC00');
    image8 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060572012022EDC00');
    image9 = ee.Image('LEDAPS/LE7_L1T_SR/LE70060582012022EDC00');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562012301ASN00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572012253EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582012253EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)

    
def GetTrendyMapId_2013():

    image1 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80040562013354LGN00');
    image2 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80040572013354LGN00');
    image3 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050552013361LGN00');
    image4 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050562013297LGN00');
    image5 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050572013297LGN00');
    image6 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060552013160LGN00');
    image7 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060562013256LGN00');
    image8 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060572013256LGN00');
    image9 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060582013256LGN00');
    image10 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070562013279LGN01');
    image11 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070572013167LGN00');
    image12 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070582013167LGN00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L8)

def GetTrendyMapId_2014():

    image1 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80040562014021LGN00');
    image2 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80040572014021LGN00');
    image3 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050552014028LGN00');
    image4 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050562014028LGN00');
    image5 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80050572014028LGN00');
    image6 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060552014243LGN00');
    image7 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060562014243LGN00');
    image8 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060572014051LGN00');
    image9 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80060582014035LGN00');
    image10 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070562014090LGN00');
    image11 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070572014090LGN00');
    image12 = ee.Image('LANDSAT/LC8_L1T_TOA/LC80070582014090LGN00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L8)

"""
def GetTrendyMapId_2015():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562001009AGS00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572001033XXX01');
    image3 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050552001008AAA02');
    image4 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050562001008AAA02');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572001008AAA02');
    image6 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060552001031XXX01');
    image7 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060562001047XXX01');
    image8 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060572001047XXX01');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582001031XXX01');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562001030AGS00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572001062EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582001062EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)
    
def GetTrendyMapId_2016():

    image1 = ee.Image('LEDAPS/LE7_L1T_SR/LE70040562001009AGS00');
    image2 = ee.Image('LEDAPS/LT5_L1T_SR/LT50040572001033XXX01');
    image3 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050552001008AAA02');
    image4 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050562001008AAA02');
    image5 = ee.Image('LEDAPS/LT5_L1T_SR/LT50050572001008AAA02');
    image6 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060552001031XXX01');
    image7 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060562001047XXX01');
    image8 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060572001047XXX01');
    image9 = ee.Image('LEDAPS/LT5_L1T_SR/LT50060582001031XXX01');
    image10 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070562001030AGS00');
    image11 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070572001062EDC00');
    image12 = ee.Image('LEDAPS/LE7_L1T_SR/LE70070582001062EDC00');

    collection = ee.ImageCollection.fromImages([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12]);
    return collection.getMapId(vizParams_L5L7)
"""    


def GetValueAtPoint(lat, lon):
    global cloudiness
    g = ee.Geometry.Point([float(lon), float(lat)])
    #g = ee.Geometry.Point([-122.22599, 37.17605])
    print(g)
    res = cloudiness.reduceRegion(ee.Reducer.mean(), g, REDUCTION_SCALE_METERS)
    return json.dumps(res.getInfo())

def GetPolygonTimeSeries(polygon_id):
  """Returns details about the polygon with the passed-in ID."""
  details = memcache.get(polygon_id)

  # If we've cached details for this polygon, return them.
  if details is not None:
    return details

  details = {'wikiUrl': WIKI_URL + polygon_id.replace('-', '%20')}

  try:
    details['timeSeries'] = ComputePolygonTimeSeries(polygon_id)
    # Store the results in memcache.
    memcache.add(polygon_id, json.dumps(details), MEMCACHE_EXPIRATION)
  except ee.EEException as e:
    # Handle exceptions from the EE client library.
    details['error'] = str(e)

  # Send the results to the browser.
  return json.dumps(details)


def ComputePolygonTimeSeries(polygon_id):
  """Returns a series of brightness over time for the polygon."""
  collection = ee.ImageCollection(IMAGE_COLLECTION_ID)
  collection = collection.select('stable_lights').sort('system:time_start')
  feature = GetFeature(polygon_id)

  # Compute the mean brightness in the region in each image.
  def ComputeMean(img):
    reduction = img.reduceRegion(
        ee.Reducer.mean(), feature.geometry(), REDUCTION_SCALE_METERS)
    return ee.Feature(None, {
        'stable_lights': reduction.get('stable_lights'),
        'system:time_start': img.get('system:time_start')
    })
  chart_data = collection.map(ComputeMean).getInfo()

  # Extract the results as a list of lists.
  def ExtractMean(feature):
    return [
        feature['properties']['system:time_start'],
        feature['properties']['stable_lights']
    ]
  return map(ExtractMean, chart_data['features'])


def GetFeature(polygon_id):
  """Returns an ee.Feature for the polygon with the given ID."""
  # Note: The polygon IDs are read from the filesystem in the initialization
  # section below. "sample-id" corresponds to "static/polygons/sample-id.json".
  path = POLYGON_PATH + polygon_id + '.json'
  path = os.path.join(os.path.split(__file__)[0], path)
  with open(path) as f:
    return ee.Feature(json.load(f))


###############################################################################
#                                   Constants.                                #
###############################################################################


# Memcache is used to avoid exceeding our EE quota. Entries in the cache expire
# 24 hours after they are added. See:
# https://cloud.google.com/appengine/docs/python/memcache/
MEMCACHE_EXPIRATION = 60 * 60 * 24

# The ImageCollection of the night-time lights dataset. See:
# https://earthengine.google.org/#detail/NOAA%2FDMSP-OLS%2FNIGHTTIME_LIGHTS
IMAGE_COLLECTION_ID = 'NOAA/DMSP-OLS/NIGHTTIME_LIGHTS'

# The file system folder path to the folder with GeoJSON polygon files.
POLYGON_PATH = 'static/polygons/'

# The scale at which to reduce the polygons for the brightness time series.
REDUCTION_SCALE_METERS = 20000

# The Wikipedia URL prefix.
WIKI_URL = 'http://en.wikipedia.org/wiki/'

vizParams_L5L7 = {'min':0,'max':4000, 'bands': 'B4,B5,B3'}
vizParams_L8 = {'min':0,'max':0.4, 'bands': 'B5,B6,B4'}

###############################################################################
#                               Initialization.                               #
###############################################################################


# Use our App Engine service account's credentials.
EE_CREDENTIALS = ee.ServiceAccountCredentials(
    config.EE_ACCOUNT, config.EE_PRIVATE_KEY_FILE)

# Read the polygon IDs from the file system.
POLYGON_IDS = [name.replace('.json', '') for name in os.listdir(POLYGON_PATH)]

# Create the Jinja templating system we use to dynamically generate HTML. See:
# http://jinja.pocoo.org/docs/dev/
JINJA2_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

# Initialize the EE API.
ee.Initialize(EE_CREDENTIALS)
