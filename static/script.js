/**
 * @fileoverview Runs the Trendy Lights application. The code is executed in the
 * user's browser. It communicates with the App Engine backend, renders output
 * to the screen, and handles user interactions.
 */


trendy = {};  // Our namespace.

var checked = "checked";

/**
 * Starts the Trendy Lights application. The main entry point for the app.
 * @param {string} eeMapId The Earth Engine map ID.
 * @param {string} eeToken The Earth Engine map token.
 * @param {string} serializedPolygonIds A serialized array of the IDs of the
 *     polygons to show on the map. For example: "['poland', 'moldova']".
 */
trendy.boot = function(eeMapId_2000, eeToken_2000, eeMapId_2001, eeToken_2001, eeMapId_2002, eeToken_2002, eeMapId_2003, eeToken_2003, eeMapId_2004, eeToken_2004, eeMapId_2005, eeToken_2005, eeMapId_2006, eeToken_2006, eeMapId_2007, eeToken_2007, eeMapId_2008, eeToken_2008, eeMapId_2009, eeToken_2009, eeMapId_2010, eeToken_2010, eeMapId_2011, eeToken_2011, eeMapId_2012, eeToken_2012, eeMapId_2013, eeToken_2013, eeMapId_2014, eeToken_2014, serializedPolygonIds) {
  // Load external libraries.
  google.load('visualization', '1.0');
  google.load('jquery', '1');
  google.load('maps', '3');

  // Create the Trendy Lights app.
  google.setOnLoadCallback(function() {
    var mapType_2000 = trendy.App.getEeMapType(eeMapId_2000, eeToken_2000);
    var mapType_2001 = trendy.App.getEeMapType(eeMapId_2001, eeToken_2001);
    var mapType_2002 = trendy.App.getEeMapType(eeMapId_2002, eeToken_2002);
    var mapType_2003 = trendy.App.getEeMapType(eeMapId_2003, eeToken_2003);
    var mapType_2004 = trendy.App.getEeMapType(eeMapId_2004, eeToken_2004);
    var mapType_2005 = trendy.App.getEeMapType(eeMapId_2005, eeToken_2005);
    var mapType_2006 = trendy.App.getEeMapType(eeMapId_2006, eeToken_2006);
    var mapType_2007 = trendy.App.getEeMapType(eeMapId_2007, eeToken_2007);
    var mapType_2008 = trendy.App.getEeMapType(eeMapId_2008, eeToken_2008);
    var mapType_2009 = trendy.App.getEeMapType(eeMapId_2009, eeToken_2009);
    var mapType_2010 = trendy.App.getEeMapType(eeMapId_2010, eeToken_2010);
    var mapType_2011 = trendy.App.getEeMapType(eeMapId_2011, eeToken_2011);
    var mapType_2012 = trendy.App.getEeMapType(eeMapId_2012, eeToken_2012);
    var mapType_2013 = trendy.App.getEeMapType(eeMapId_2013, eeToken_2013);
    var mapType_2014 = trendy.App.getEeMapType(eeMapId_2014, eeToken_2014);
    /*var mapType_2015 = trendy.App.getEeMapType(eeMapId_2015, eeToken_2015);*/
    /*var mapType_2016 = trendy.App.getEeMapType(eeMapId_2016, eeToken_2016);*/
    var app = new trendy.App(mapType_2000, mapType_2001, mapType_2002, mapType_2003, mapType_2004, mapType_2005, mapType_2006, mapType_2007, mapType_2008, mapType_2009, mapType_2010, mapType_2011, mapType_2012, mapType_2013, mapType_2014, JSON.parse(serializedPolygonIds));
  });
};


///////////////////////////////////////////////////////////////////////////////
//                               The application.                            //
///////////////////////////////////////////////////////////////////////////////



/**
 * The main Trendy Lights application.
 * This constructor renders the UI and sets up event handling.
 * @param {google.maps.ImageMapType} mapType The map type to render on the map.
 * @param {Array<string>} polygonIds The IDs of the polygons to show on the map.
 *     For example ['poland', 'moldova', 'llanos'].
 * @constructor
 */
trendy.App = function(mapType_2000, mapType_2001, mapType_2002, mapType_2003, mapType_2004, mapType_2005, mapType_2006, mapType_2007, mapType_2008, mapType_2009, mapType_2010, mapType_2011, mapType_2012, mapType_2013, mapType_2014, polygonIds) {
  // Create and display the map.
  this.map = this.createMap();
  
  // Add place holders
  this.map.overlayMapTypes.push(null);  // 2000
  this.map.overlayMapTypes.push(null);  // 2001
  this.map.overlayMapTypes.push(null);  // 2002
  this.map.overlayMapTypes.push(null);  // 2003
  this.map.overlayMapTypes.push(null);  // 2004
  this.map.overlayMapTypes.push(null);  // 2005
  this.map.overlayMapTypes.push(null);  // 2006
  this.map.overlayMapTypes.push(null);  // 2007
  this.map.overlayMapTypes.push(null);  // 2008
  this.map.overlayMapTypes.push(null);  // 2009
  this.map.overlayMapTypes.push(null);  // 2010
  this.map.overlayMapTypes.push(null);  // 2011
  this.map.overlayMapTypes.push(null);  // 2012
  this.map.overlayMapTypes.push(null);  // 2013
  this.map.overlayMapTypes.push(null);  // 2014
  //this.map.overlayMapTypes.push(null);  // 2015
  //this.map.overlayMapTypes.push(null);  // 2016

  //var x2000 = $('#myCheck2000').is(':checked');
  //var xPoly = $('#myCheckPoly').is(':checked');
  
  //if(x2000 === true){
  //this.map.overlayMapTypes.push(mapType);
  
  if($('#myCheck2000').is(':checked')){
  this.map.overlayMapTypes.setAt(0, mapType_2000);
  }
  
  if($('#myCheck2001').is(':checked')){
    this.map.overlayMapTypes.setAt(1, mapType_2001);
  }
  
  if($('#myCheck2002').is(':checked')){
    this.map.overlayMapTypes.setAt(2, mapType_2002);
  }
  
  if($('#myCheck2003').is(':checked')){
    this.map.overlayMapTypes.setAt(3, mapType_2003);
  }
  
  if($('#myCheck2004').is(':checked')){
    this.map.overlayMapTypes.setAt(4, mapType_2004);
  }
  
  if($('#myCheck2005').is(':checked')){
    this.map.overlayMapTypes.setAt(5, mapType_2005);
  }
  
  if($('#myCheck2006').is(':checked')){
    this.map.overlayMapTypes.setAt(6, mapType_2006);
  }
  
  if($('#myCheck2007').is(':checked')){
    this.map.overlayMapTypes.setAt(7, mapType_2007);
  }
  
  if($('#myCheck2008').is(':checked')){
    this.map.overlayMapTypes.setAt(8, mapType_2008);
  }
  
  if($('#myCheck2009').is(':checked')){
    this.map.overlayMapTypes.setAt(9, mapType_2009);
  }
  
  if($('#myCheck2010').is(':checked')){
    this.map.overlayMapTypes.setAt(10, mapType_2010);
  }
  
  if($('#myCheck2011').is(':checked')){
    this.map.overlayMapTypes.setAt(11, mapType_2011);
  }
  
  if($('#myCheck2012').is(':checked')){
    this.map.overlayMapTypes.setAt(12, mapType_2012);
  }
  
  if($('#myCheck2013').is(':checked')){
    this.map.overlayMapTypes.setAt(13, mapType_2013);
  }
  
  if($('#myCheck2014').is(':checked')){
    this.map.overlayMapTypes.setAt(14, mapType_2014);
  }
  
  //if($('#myCheck2015').is(':checked')){
  //  this.map.overlayMapTypes.setAt(15, mapType_2015);
  //}
  
  //if($('#myCheck2016').is(':checked')){
  //  this.map.overlayMapTypes.setAt(16, mapType_2016);
  //}
  
  //if(xPoly === true){
  // Add the polygons to the map.
  if($('#myCheckPoly').is(':checked')){
  this.addPolygons(polygonIds);
  }
  
  $('#myCheck2000').click((function() {
    if($('#myCheck2000').is(':checked')){
    //$('.panel .title').show().text(checked + 'tt ' + mapType_2000.index);
  this.map.overlayMapTypes.setAt(0, mapType_2000);
    }
   else{
      //$('.panel .title').show().text(checked + 'off');
      //this.map.overlayMapTypes.removeAt(0);
      this.map.overlayMapTypes.setAt(0, null);
   }
  }).bind(this));
  
$('#myCheck2001').click((function() {
if($('#myCheck2001').is(':checked')){
this.map.overlayMapTypes.setAt(1, mapType_2001);
}
else{
this.map.overlayMapTypes.setAt(1, null);
}
}).bind(this));

$('#myCheck2002').click((function() {
if($('#myCheck2002').is(':checked')){
this.map.overlayMapTypes.setAt(2, mapType_2002);
}
else{
this.map.overlayMapTypes.setAt(2, null);
}
}).bind(this));

$('#myCheck2003').click((function() {
if($('#myCheck2003').is(':checked')){
this.map.overlayMapTypes.setAt(3, mapType_2003);
}
else{
this.map.overlayMapTypes.setAt(3, null);
}
}).bind(this));

$('#myCheck2004').click((function() {
if($('#myCheck2004').is(':checked')){
this.map.overlayMapTypes.setAt(4, mapType_2004);
}
else{
this.map.overlayMapTypes.setAt(4, null);
}
}).bind(this));

$('#myCheck2005').click((function() {
if($('#myCheck2005').is(':checked')){
this.map.overlayMapTypes.setAt(5, mapType_2005);
}
else{
this.map.overlayMapTypes.setAt(5, null);
}
}).bind(this));

$('#myCheck2006').click((function() {
if($('#myCheck2006').is(':checked')){
this.map.overlayMapTypes.setAt(6, mapType_2006);
}
else{
this.map.overlayMapTypes.setAt(6, null);
}
}).bind(this));

$('#myCheck2007').click((function() {
if($('#myCheck2007').is(':checked')){
this.map.overlayMapTypes.setAt(7, mapType_2007);
}
else{
this.map.overlayMapTypes.setAt(7, null);
}
}).bind(this));

$('#myCheck2008').click((function() {
if($('#myCheck2008').is(':checked')){
this.map.overlayMapTypes.setAt(8, mapType_2008);
}
else{
this.map.overlayMapTypes.setAt(8, null);
}
}).bind(this));

$('#myCheck2009').click((function() {
if($('#myCheck2009').is(':checked')){
this.map.overlayMapTypes.setAt(9, mapType_2009);
}
else{
this.map.overlayMapTypes.setAt(9, null);
}
}).bind(this));

$('#myCheck2010').click((function() {
if($('#myCheck2010').is(':checked')){
this.map.overlayMapTypes.setAt(10, mapType_2010);
}
else{
this.map.overlayMapTypes.setAt(10, null);
}
}).bind(this));

$('#myCheck2011').click((function() {
if($('#myCheck2011').is(':checked')){
this.map.overlayMapTypes.setAt(11, mapType_2011);
}
else{
this.map.overlayMapTypes.setAt(11, null);
}
}).bind(this));

$('#myCheck2012').click((function() {
if($('#myCheck2012').is(':checked')){
this.map.overlayMapTypes.setAt(12, mapType_2012);
}
else{
this.map.overlayMapTypes.setAt(12, null);
}
}).bind(this));

$('#myCheck2013').click((function() {
if($('#myCheck2013').is(':checked')){
this.map.overlayMapTypes.setAt(13, mapType_2013);
}
else{
this.map.overlayMapTypes.setAt(13, null);
}
}).bind(this));

$('#myCheck2014').click((function() {
if($('#myCheck2014').is(':checked')){
this.map.overlayMapTypes.setAt(14, mapType_2014);
}
else{
this.map.overlayMapTypes.setAt(14, null);
}
}).bind(this));

/**
$('#myCheck2015').click((function() {
if($('#myCheck2015').is(':checked')){
this.map.overlayMapTypes.setAt(15, mapType_2015);
}
else{
this.map.overlayMapTypes.removeAt(15);
this.map.overlayMapTypes.setAt(15, null);
}
}).bind(this));

$('#myCheck2016').click((function() {
if($('#myCheck2016').is(':checked')){
this.map.overlayMapTypes.setAt(16, mapType_2016);
}
else{
this.map.overlayMapTypes.removeAt(16);
this.map.overlayMapTypes.setAt(16, null);
}
}).bind(this));
 */

  /*
  $('#myCheck2000').click((function() {
    if($('#myCheck2000').is(':checked')){
      this.map.overlayMapTypes.setAt(0, mapType);
      $('.panel .title').show().text(checked + 'tt');
   }
   else{
      this.map.overlayMapTypes.removeAt(0);
   }
    //$('.panel').toggleClass('expanded');
  })); //}).bind(this));
  */
  // Register a click handler to show a panel when the user clicks on a place.
  // this.map.data.addListener('click', this.handlePolygonClick.bind(this));
  
  // Show panel
  //  if(x2000 === true){checked = x2000;}
    $('.panel').show();
  // $('.panel .title').show().text(title);
  //$('.panel .title').show().text(checked);

  // Register a click handler to hide the panel when the user clicks close.
  $('.panel .close').click(this.hidePanel.bind(this));

  // Register a click handler to expand the panel when the user taps on toggle.
  $('.panel .toggler').click((function() {
    $('.panel').toggleClass('expanded');
  }).bind(this));
};

/**
 * Creates a Google Map with a black background the given map type rendered.
 * The map is anchored to the DOM element with the CSS class 'map'.
 * @param {google.maps.ImageMapType} mapType The map type to include on the map.
 * @return {google.maps.Map} A map instance with the map type rendered.
 */
//trendy.App.prototype.createMap = function(mapType) {
trendy.App.prototype.createMap = function() {
  var mapOptions = {
    backgroundColor: '#000000',
    center: trendy.App.DEFAULT_CENTER,
    disableDefaultUI: false,
    zoom: trendy.App.DEFAULT_ZOOM,
    scaleControl: true
  };
  var mapEl = $('.map').get(0);
  var map = new google.maps.Map(mapEl, mapOptions);
  map.setOptions({styles: trendy.App.BLACK_BASE_MAP_STYLES});
  //map.overlayMapTypes.push(mapType);
  return map;
};


/**
 * Adds the polygons with the passed-in IDs to the map.
 * @param {Array<string>} polygonIds The IDs of the polygons to show on the map.
 *     For example ['poland', 'moldova'].
 */
trendy.App.prototype.addPolygons = function(polygonIds) {
  polygonIds.forEach((function(polygonId) {
    this.map.data.loadGeoJson('static/polygons/' + polygonId + '.json');
  }).bind(this));
  this.map.data.setStyle(function(feature) {
    return {
      fillColor: 'white',
      fillOpacity:0,
      strokeColor: 'white',
      strokeWeight: 3
    };
  });
};


/**
 * Handles a on click a polygon. Highlights the polygon and shows details about
 * it in a panel.
 * @param {Object} event The event object, which contains details about the
 *     polygon clicked.
 */
trendy.App.prototype.handlePolygonClick = function(event) {
  this.clear();
  var feature = event.feature;
  
    var x = $('#myCheck2000').is(':checked');
    //var x = $('#myCheck2000')[0];
    //$('demo')).innerHTML = x;
    if(x === true){checked = x;}
    

  // Instantly higlight the polygon and show the title of the polygon.
  this.map.data.overrideStyle(feature, {strokeWeight: 4});
  var title = feature.getProperty('title');
  $('.panel').show();
  // $('.panel .title').show().text(title);
  //$('.panel .title').show().text(checked);
  $('.panel .wiki-url').show().attr('href', 'wikiUrl');


  // Asynchronously load and show details about the polygon.
  var id = feature.getProperty('id');
  $.get('/details?polygon_id=' + id).done((function(data) {
    if (data['error']) {
      $('.panel .error').show().html(data['error']);
    } else {
      $('.panel .wiki-url').show().attr('href', data['wikiUrl']);
      
      this.showChart(data['timeSeries']);
    }
  }).bind(this));
};


/** Clears the details panel and selected polygon. */
trendy.App.prototype.clear = function() {
  $('.panel .title').empty().hide();
  $('.panel .wiki-url').hide().attr('href', '');
  $('.panel .chart').empty().hide();
  $('.panel .error').empty().hide();
  $('.panel').hide();
  this.map.data.revertStyle();
};


/** Hides the details panel. */
trendy.App.prototype.hidePanel = function() {
  $('.panel').hide();
  this.clear();
};


/**
 * Shows a chart with the given timeseries.
 * @param {Array<Array<number>>} timeseries The timeseries data
 *     to plot in the chart.
 */
trendy.App.prototype.showChart = function(timeseries) {
  timeseries.forEach(function(point) {
    point[0] = new Date(parseInt(point[0], 10));
  });
  var data = new google.visualization.DataTable();
  data.addColumn('date');
  data.addColumn('number');
  data.addRows(timeseries);
  var wrapper = new google.visualization.ChartWrapper({
    chartType: 'LineChart',
    dataTable: data,
    options: {
      title: 'Brightness over time',
      curveType: 'function',
      legend: {position: 'none'},
      titleTextStyle: {fontName: 'Roboto'}
    }
  });
  $('.panel .chart').show();
  var chartEl = $('.chart').get(0);
  wrapper.setContainerId(chartEl);
  wrapper.draw();
};


///////////////////////////////////////////////////////////////////////////////
//                        Static helpers and constants.                      //
///////////////////////////////////////////////////////////////////////////////


/**
 * Generates a Google Maps map type (or layer) for the passed-in EE map id. See:
 * https://developers.google.com/maps/documentation/javascript/maptypes#ImageMapTypes
 * @param {string} eeMapId The Earth Engine map ID.
 * @param {string} eeToken The Earth Engine map token.
 * @return {google.maps.ImageMapType} A Google Maps ImageMapType object for the
 *     EE map with the given ID and token.
 */
trendy.App.getEeMapType = function(eeMapId, eeToken) {
  var eeMapOptions = {
    getTileUrl: function(tile, zoom) {
      var url = trendy.App.EE_URL + '/map/';
      url += [eeMapId, zoom, tile.x, tile.y].join('/');
      url += '?token=' + eeToken;
      return url;
    },
    tileSize: new google.maps.Size(256, 256)
  };
  return new google.maps.ImageMapType(eeMapOptions);
};


/** @type {string} The Earth Engine API URL. */
trendy.App.EE_URL = 'https://earthengine.googleapis.com';


/** @type {number} The default zoom level for the map. */
trendy.App.DEFAULT_ZOOM = 7;


/** @type {Object} The default center of the map. */
trendy.App.DEFAULT_CENTER = {lng: -70.64994, lat: 4.842728};


/**
 * @type {Array} An array of Google Map styles. See:
 *     https://developers.google.com/maps/documentation/javascript/styling
 */
trendy.App.BLACK_BASE_MAP_STYLES = [
  {stylers: [{lightness: 0}]},
  {
    featureType: 'road',
    elementType: 'labels',
    stylers: [{visibility: 'off'}]
  }
];
