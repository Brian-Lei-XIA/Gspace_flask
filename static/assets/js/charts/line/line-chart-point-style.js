function createConfig(pointStyle) {
	return {
		type: 'line',
		data: {
			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
			datasets: [{
				label: 'My First dataset',
				backgroundColor: window.chartColors.red,
				borderColor: window.chartColors.red,
				data: [10, 23, 5, 99, 67, 43, 0],
				fill: false,
				pointRadius: 10,
				pointHoverRadius: 15,
				showLine: false // no line shown
			}]
		},
		options: {
			maintainAspectRatio: false,
			responsive: true,
			title: {
				display: false,
				text: 'Point Style: ' + pointStyle
			},
			legend: {
				display: false
			},
			elements: {
				point: {
					pointStyle: pointStyle
				}
			}
		}
	};
}

window.onload = function() {
	var container = document.querySelector('.line-point-chart');
	['circle'].forEach(function(pointStyle) {
		var div = document.createElement('div');
		div.classList.add('chart-container');

		var canvas = document.createElement('canvas');
		div.appendChild(canvas);
		container.appendChild(div);

		var ctx = canvas.getContext('2d');
		var config = createConfig(pointStyle);
		new Chart(ctx, config);
	});
};