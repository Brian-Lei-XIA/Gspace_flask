new Chart(document.getElementById("multiline-pie-chart"), {
    type: 'pie',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
            label: "Population (millions)",
            data: [65, 59, 80, 81, 56],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0", "#FFCD56", "#F39346"],
        }, {
            label: "Population (millions)",
            data: [28, 48, 40, 19, 86],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0", "#FFCD56", "#F39346"],
        }, {
            label: "Population (millions)",
            data: [45, 25, 16, 36, 67],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0", "#FFCD56", "#F39346"],
        }, {
            label: "Population (millions)",
            data: [17, 62, 78, 88, 26],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0", "#FFCD56", "#F39346"],
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
