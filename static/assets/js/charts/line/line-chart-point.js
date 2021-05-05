new Chart(document.getElementById("line-chart-point"), {
    type: 'line',
    data: {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [{
			label: 'dataset - big points',
			fill: false,
			data: [70, 28, 75, -59, -31, 96, -38],
			backgroundColor: window.chartColors.red,
			borderColor: window.chartColors.red,
			borderDash: [5, 5],
			pointRadius: 15,
			pointHoverRadius: 10,
		}, {
			label: 'dataset - individual point sizes',
			fill: false,
			data: [-46, -12, 15, 67, -15, -10],
			backgroundColor: window.chartColors.blue,
			borderColor: window.chartColors.blue,
			fill: false,
			borderDash: [5, 5],
			pointRadius: [2, 4, 6, 18, 0, 12, 20],
		}, {
			label: 'dataset - large pointHoverRadius',
			data: [-78, -46, 7, -70, 6, 2, -57],
			backgroundColor: window.chartColors.green,
			borderColor: window.chartColors.green,
			fill: false,
			pointHoverRadius: 30,
		}, {
			label: 'dataset - large pointHitRadius',
			data: [24, 57, 44, 92, 56, -83, 96],
			backgroundColor: window.chartColors.yellow,
			borderColor: window.chartColors.yellow,
			fill: false,
			pointHitRadius: 20,
		}]
	},
    options: {
		maintainAspectRatio: false,
		responsive: true,
		
		hover: {
			mode: 'index'
		},
		scales: {
			xAxes: [{
				display: false,
				scaleLabel: {
					display: true,
					labelString: 'Month'
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Value'
				}
			}]
		},
		title: {
			display: false,
			text: 'Chart.js Line Chart - Different point sizes'
		}
	}
});
