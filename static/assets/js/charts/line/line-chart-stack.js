new Chart(document.getElementById("line-chart-stack"), {
    type: 'line',
    data: {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [{
			label: 'My First Dataset',
			data: [-73, -48, 93, 73, -61, -25, -53],
			backgroundColor: window.chartColors.red,
			borderColor: window.chartColors.red,
		}, {
			label: 'My Second Dataset',
			data: [49, -28, 31, 61, -31, 9, -37],
			backgroundColor: window.chartColors.blue,
			borderColor: window.chartColors.blue,
		}, {
			label: 'My Third Dataset',
			data: [81, -35, 71, 95, -19, 67, -9],
			backgroundColor: window.chartColors.green,
			borderColor: window.chartColors.green,
		}, {
			label: 'My Fourth Dataset',
			data: [-58, 34, 19, -71, 57, 64, 28],
			backgroundColor: window.chartColors.yellow,
			borderColor: window.chartColors.yellow,
		}]
	},
    options: {
		maintainAspectRatio: false,
		responsive: true,
		title: {
			display: false,
			text: 'Chart.js Line Chart - Stacked Area'
		},
		tooltips: {
			mode: 'index',
		},
		hover: {
			mode: 'index'
		},
		scales: {
			xAxes: [{
				scaleLabel: {
					display: false,
					labelString: 'Month'
				}
			}],
			yAxes: [{
				stacked: true,
				scaleLabel: {
					display: true,
					labelString: 'Value'
				}
			}]
		}
	}
});
