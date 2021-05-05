jQuery(document).ready(function () {
	jQuery('#vmap').vectorMap({
		map: 'world_en',
		backgroundColor: '#fff',
		color: '#ffffff',
		hoverOpacity: 0.7,
		selectedColor: '#000000',
		enableZoom: true,
		showTooltip: true,
		scaleColors: ['#555555', '#CCCCCC'],
		values: sample_data,
		normalizeFunction: 'polynomial'
	});
});
new Chart(document.getElementById("vertical-bar-chart"), {
    type: 'bar',
    data: {
		labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
		datasets: [
			{
				label: "Sales",
				backgroundColor: ["#237EE5", "#888888","#237EE5","#888888","#237EE5","#888888","#888888"],
				data: [2478,5267,734,784,433,784,433]
			}
		]
    },
    options: {
		maintainAspectRatio: false,
		responsive:true,
		legend: { display: false },
		title: {
		display: true,
			text: 'Predicted last week sales'
		}	
    }
	
});
new Chart(document.getElementById("pie-chart"), {
    type: 'pie',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
        label: "Revenues ($)",
        backgroundColor: ["#237EE5", "#888888","#237EE5","#888888","#237EE5"],
        data: [2478,5267,734,784,433]
      }]
    },
    options: {
	  maintainAspectRatio: false,
	  responsive: true,
	  legend: { display: false },
      title: {
        display: true,
        text: 'Predicted Revenues in $'
      }
    }
});
