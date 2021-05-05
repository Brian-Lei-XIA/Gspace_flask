$(function() {
	// Example Data

	var data = [
		{ label: "Series1",  data: 20},
		{ label: "Series2",  data: 90},
		{ label: "Series3",  data: 70},
		{ label: "Series4",  data: 80},
		{ label: "Series5",  data: 110}
	];

	var placeholder = $("#placeholder");
		$.plot('#placeholder', data, {
		series: {
			pie: {
				show: true,
				radius: 1,
				label: {
					show: true,
					radius: 3/4,
					formatter: labelFormatter,
					background: {
						opacity: 0
					}
				}
			}
		},
		legend: {
			show: false
		},
		grid: {
			hoverable: true,
			clickable: true
		}
	});
});

// A custom label formatter used by several of the plots
function labelFormatter(label, series) {
	return "<div style='font-size:0.7rem; text-align:center; padding:2px; color:white;'>" + label + "<br/>" + Math.round(series.percent) + "%</div>";
}
//