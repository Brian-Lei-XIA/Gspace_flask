new Chart(document.getElementById("multi-axies-bar"), {
    type: 'bar',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
		label: 'Dataset 1',
		backgroundColor: ["#FF6384", "#36A2EB","#4BC0C0","#FFCD56","#F39346"],
		yAxisID: 'y-axis-1',
			data: [3478,5267,3734,4784,5433]
		}, {
		label: 'Dataset 2',
		backgroundColor: window.chartColors.grey,
		yAxisID: 'y-axis-2',
			data: [-10000,-11000,734,-8000,433]
		}]
    },
	options: {
		maintainAspectRatio: false,
		responsive:true,
		title: {
			display: true,
			text: 'Chart.js Bar Chart - Multi Axis'
		},
		tooltips: {
			mode: 'index',
			intersect: true
		},
		scales: {
			yAxes: [{
				type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
				display: true,
				position: 'left',
				id: 'y-axis-1',
			}, {
				type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
				display: true,
				position: 'right',
				id: 'y-axis-2',
				gridLines: {
					drawOnChartArea: false
				}
			}],
		}
	}
});