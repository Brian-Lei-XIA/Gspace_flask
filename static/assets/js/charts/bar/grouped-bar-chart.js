new Chart(document.getElementById("grouped-bar-chart"), {
    type: 'bar',
    data: {
      labels: ["1900", "1950", "1999", "2050"],
      datasets: [
        {
          label: "Africa",
          backgroundColor: "#FF6384",
          data: [133,221,783,2478]
        }, {
          label: "Europe",
          backgroundColor: "#36A2EB",
          data: [408,547,675,734]
        }
      ]
    },
    options: {
	  maintainAspectRatio: false,
	  responsive:true,
      title: {
        display: true,
        text: 'Population growth (millions)'
      }
    }
});