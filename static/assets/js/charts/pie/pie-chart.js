new Chart(document.getElementById("pie-chart"), {
    type: 'pie',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#FF6384", "#36A2EB","#4BC0C0","#FFCD56","#F39346"],
        data: [2478,5267,734,784,433]
      }]
    },
    options: {
	  maintainAspectRatio: false,
	  responsive: true,
      title: {
        display: true,
        text: 'Predicted world population (millions) in 2050'
      }
    }
});
