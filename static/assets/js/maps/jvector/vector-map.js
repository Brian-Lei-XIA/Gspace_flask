jQuery(document).ready(function () {
	jQuery('#vmap').vectorMap({
		map: 'world_en',
		backgroundColor: '#fff',
		color: '#ffffff',
		hoverOpacity: 0.7,
		selectedColor: '#666666',
		enableZoom: true,
		showTooltip: true,
		scaleColors: ['#C8EEFF', '#006491'],
		values: sample_data,
		normalizeFunction: 'polynomial'
	});
});
jQuery(document).ready(function () {
	jQuery('#label-vmap').vectorMap({
		map: 'usa_en',
		borderWidth: 0.25,
		showLabels: true
	});
});
var map;

      jQuery(document).ready(function () {

        // Store currentRegion
        var currentRegion = 'fl';

        // List of Regions we'll let clicks through for
        var enabledRegions = ['mo', 'fl', 'or'];

        map = jQuery('#inactive-vmap').vectorMap({
          map: 'usa_en',
          enableZoom: true,
          showTooltip: true,
          selectedColor: '#333333',
          selectedRegions: ['fl'],
          hoverColor: null,
          colors: {
            mo: '#DD8627',
            fl: '#DD8627',
            or: '#DD8627'
          },
          onRegionClick: function(event, code, region){
            // Check if this is an Enabled Region, and not the current selected on
            if(enabledRegions.indexOf(code) === -1 || currentRegion === code){
              // Not an Enabled Region
              event.preventDefault();
            } else {
              // Enabled Region. Update Newly Selected Region.
              currentRegion = code;
            }
          },
          onRegionSelect: function(event, code, region){
            console.log(map.selectedRegions);
          },
          onLabelShow: function(event, label, code){
            if(enabledRegions.indexOf(code) === -1){
              event.preventDefault();
            }
          }
        });
      });
	  jQuery('#vmap-asia').vectorMap({
          map: 'asia_en',
          backgroundColor: '#fff',
          color: '#ffffff',
          hoverOpacity: 0.7,
          selectedColor: '#666666',
          enableZoom: true,
          showTooltip: true,
          values: sample_data,
          scaleColors: ['#0061ff', '#79b2cc'],
          normalizeFunction: 'polynomial'
        });
		jQuery('#vmap-africa').vectorMap({
          map: 'africa_en',
          backgroundColor: '#fff',
          color: '#ffffff',
          hoverOpacity: 0.7,
          selectedColor: '#666666',
          enableZoom: true,
          showTooltip: true,
          values: sample_data,
          scaleColors: ['#3450cf', '#591b98'],
          normalizeFunction: 'polynomial'
        });
		jQuery('#vmap-australia').vectorMap({
          map: 'australia_en',
          backgroundColor: '#fff',
          color: '#ffffff',
          hoverOpacity: 0.7,
          selectedColor: '#666666',
          enableZoom: true,
          showTooltip: true,
          values: sample_data,
          scaleColors: ['#1a4695', '#771060'],
          normalizeFunction: 'polynomial'
        });