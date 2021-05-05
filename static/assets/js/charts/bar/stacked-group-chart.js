new Chart(document.getElementById("stacked-group-chart"), {
    type: 'bar',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [
        {
          label: "Dataset 1",
          backgroundColor: "#FF6384",
		  stack: 'Stack 0',
          data: [3478,5267,3734,4784,5433]
        },
		{
          label: "Dataset 2",
          backgroundColor: "#36A2EB",
		  stack: 'Stack 0',
          data: [2478,5267,734,784,433]
        },
		{
          label: "Dataset 3",
          backgroundColor: "#4BC0C0",
		  stack: 'Stack 1',
          data: [-10000,-11000,734,-8000,433]
        }
      ]
    },
    options: {
		maintainAspectRatio: false,
		responsive:true,
		title: {
			display: true,
			text: 'Chart.js Bar Chart - Stacked'
		},
		tooltips: {
			mode: 'index',
			intersect: false
		},
		responsive: true,
		scales: {
			xAxes: [{
				stacked: true,
			}],
			yAxes: [{
				stacked: true
			}]
		}
	}
});