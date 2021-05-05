+function ($) {
  'use strict';
	
	map = new GMaps({
        el: '#map',
        lat: -12.043333,
        lng: -77.028333,
        zoomControl : true,
        zoomControlOpt: {
            style : 'SMALL',
            position: 'TOP_LEFT'
		},
		panControl : false,
		streetViewControl : false,
		mapTypeControl: false,
		overviewMapControl: false
	});
	
	map = new GMaps({
        el: '#map-marker',
        lat: -12.043333,
        lng: -77.028333
	});
	map.addMarker({
        lat: -12.043333,
        lng: -77.03,
        title: 'Lima',
        details: {
          database_id: 42,
          author: 'HPNeo'
        },
        click: function(e){
          if(console.log)
            console.log(e);
          alert('You clicked in this marker');
        },
        mouseover: function(e){
          if(console.log)
            console.log(e);
        }
	});
	map.addMarker({
        lat: -12.042,
        lng: -77.028333,
        title: 'Marker with InfoWindow',
        infoWindow: {
          content: '<p>HTML Content</p>'
        }
	});
	
	var map = new GMaps({
          el: "#map-style",
          lat: 41.895465,
          lng: 12.482324,
          zoom: 5, 
          zoomControl : true,
          zoomControlOpt: {
            style : "SMALL",
            position: "TOP_LEFT"
          },
          panControl : true,
          streetViewControl : false,
          mapTypeControl: false,
          overviewMapControl: false
        });
        
        var styles = [
            {
              stylers: [
                { hue: "#00ffe6" },
                { saturation: -20 }
              ]
            }, {
                featureType: "road",
                elementType: "geometry",
                stylers: [
                    { lightness: 100 },
                    { visibility: "simplified" }
              ]
            }, {
                featureType: "road",
                elementType: "labels",
                stylers: [
                    { visibility: "off" }
              ]
            }
        ];
        
        map.addStyle({
            styledMapName:"Styled Map",
            styles: styles,
            mapTypeId: "map_style"  
        });
        
        map.setStyle("map_style");
}(jQuery);


var map, path, paths;
    $(document).ready(function(){
	map = new GMaps({
			el: '#map-polygon',
			lat: -12.040397656836609,
			lng: -77.03373871559225,
			click: function(e){
			console.log(e);
		}
	});

	paths = [
				[
					[
						[-105.00432014465332, 39.74732195489861],
						[-105.00715255737305, 39.74620006835170],
						[-105.00921249389647, 39.74468219277038],
						[-105.01067161560059, 39.74362625960105],
						[-105.01195907592773, 39.74290029616054],
						[-105.00989913940431, 39.74078835902781],
						[-105.00758171081543, 39.74059036160317],
						[-105.00346183776855, 39.74059036160317],
						[-105.00097274780272, 39.74059036160317],
						[-105.00062942504881, 39.74072235994946],
						[-105.00020027160645, 39.74191033368865],
						[-105.00071525573731, 39.74276830198601],
						[-105.00097274780272, 39.74369225589818],
						[-105.00097274780272, 39.74461619742136],
						[-105.00123023986816, 39.74534214278395],
						[-105.00183105468751, 39.74613407445653],
						[-105.00432014465332, 39.74732195489861]
					],	
					[
						[-105.00361204147337, 39.74354376414072],
						[-105.00301122665405, 39.74278480127163],
						[-105.00221729278564, 39.74316428375108],
						[-105.00283956527711, 39.74390674342741],
						[-105.00361204147337, 39.74354376414072]
					]
				],	
				[
					[
						[-105.00942707061768, 39.73989736613708],
						[-105.00942707061768, 39.73910536278566],
						[-105.00685214996338, 39.73923736397631],
						[-105.00384807586671, 39.73910536278566],
						[-105.00174522399902, 39.73903936209552],
						[-105.00041484832764, 39.73910536278566],
						[-105.00041484832764, 39.73979836621592],
						[-105.00535011291504, 39.73986436617916],
						[-105.00942707061768, 39.73989736613708]
					]
				]
			];

	path = [[-12.040397656836609,-77.03373871559225], [-12.040248585302038,-77.03993927003302], [-12.050047116528843,-77.02448169303511], [-12.044804866577001,-77.02154422636042]];

	map.drawPolygon({
		paths: paths,
		useGeoJSON: true,
		strokeColor: '#131540',
		strokeOpacity: 0.6,
		strokeWeight: 6
	});

	map.drawPolygon({
		paths: path,
		strokeColor: '#131540',
		strokeOpacity: 0.6,
		strokeWeight: 6
	});
});
	
	
var map;
var route;
$(document).ready(function(){
	$('#forward').attr('disabled', 'disabled');
	$('#back').attr('disabled', 'disabled');
	$('#get_route').click(function(e){
	e.preventDefault();
	map.getRoutes({
		origin: [map.markers[0].getPosition().lat(), map.markers[0].getPosition().lng()],
		destination: [map.markers[map.markers.length-1].getPosition().lat(), map.markers[map.markers.length-1].getPosition().lng()],
		callback: function(e){
			route = new GMaps.Route({
				map: map,
				route: e[0],
				strokeColor: '#336699',
				strokeOpacity: 0.5,
				strokeWeight: 10
			});
			$('#forward').removeAttr('disabled');
			$('#back').removeAttr('disabled');
		}
	});
	$('#forward').click(function(e){
		e.preventDefault();
		route.forward();

		if(route.step_count < route.steps_length)
		$('#steps').append('<li>'+route.steps[route.step_count].instructions+'</li>');
	});
	$('#back').click(function(e){
		e.preventDefault();
		route.back();

		if(route.step_count >= 0)
		$('#steps').find('li').last().remove();
	});
	});
	map = new GMaps({
		el: '#map-route',
		lat: -12.043333,
		lng: -77.028333,
		zoom: 16,
		click: function(e){
			map.addMarker({
				lat: e.latLng.lat(),
				lng: e.latLng.lng()
			});
		}
	});
});
	
	
var map;

var getTile = function(coord, zoom, ownerDocument) {
	var div = ownerDocument.createElement('div');
	div.innerHTML = coord;
	div.style.width = this.tileSize.width + 'px';
	div.style.height = this.tileSize.height + 'px';
	div.style.background = 'rgba(250, 250, 250, 0.55)';
	div.style.fontFamily = 'Monaco, Andale Mono, Courier New, monospace';
	div.style.fontSize = '10';
	div.style.fontWeight = 'bolder';
	div.style.border = 'dotted 1px #aaa';
	div.style.textAlign = 'center';
	div.style.lineHeight = this.tileSize.height + 'px';
	return div;
};

$(document).ready(function(){
	map = new GMaps({
		el: '#map-overlay',
		lat: -12.043333,
		lng: -77.028333
	});
		map.addOverlayMapType({
		index: 0,
		tileSize: new google.maps.Size(256, 256),
		getTile: getTile
	});
});