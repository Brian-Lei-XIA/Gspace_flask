new Chart(document.getElementById("line-chart-style"), {
    type: 'line',
    data: {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [{
			label: 'Unfilled',
			fill: false,
			backgroundColor: window.chartColors.blue,
			borderColor: window.chartColors.blue,
			data: [-80, 60, -48, -35, -77, 21, 70],
		}, {
			label: 'Dashed',
			fill: false,
			backgroundColor: window.chartColors.green,
			borderColor: window.chartColors.green,
			borderDash: [5, 5],
			data: [74, -61, -81, -3, -11, -4, -25],
		}, {
			label: 'Filled',
			backgroundColor: window.chartColors.red,
			borderColor: window.chartColors.red,
			data: [56, -17, 92, 23, -36, 30, -28],
			fill: true,
		}]
	},
    options: {
		maintainAspectRatio: false,
		responsive: true,
		title: {
			display: false,
			text: 'Chart.js Line Chart'
		},
		tooltips: {
			mode: 'index',
			intersect: false,
		},
		hover: {
			mode: 'nearest',
			intersect: true
		}
	}
});
