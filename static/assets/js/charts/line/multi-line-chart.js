new Chart(document.getElementById("multi-line-chart"), {
    type: 'line',
    data: {
			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
			datasets: [{
				label: 'My First dataset',
				backgroundColor: window.chartColors.red,
				borderColor: window.chartColors.red,
				data: [65, 59, 80, 81, 56],
				fill: false,
			}, {
				label: 'My Second dataset',
				fill: false,
				backgroundColor: window.chartColors.blue,
				borderColor: window.chartColors.blue,
				data: [28, 48, 40, 19, 86],
			}, {
				label: 'My Third dataset',
				fill: false,
				backgroundColor: window.chartColors.yellow,
				borderColor: window.chartColors.yellow,
				data: [18, 8, 4, 9, 78],
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
		},
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: {
					display: false,
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
		}
	}
});
