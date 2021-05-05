// Without JQuery
var slider = new Slider('#ex1', {
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

// Without JQuery
var slider = new Slider('#ex2', {});

// Without JQuery
var slider = new Slider('#ex5');

$("#destroyEx5Slider").click(function() {

	// Without JQuery
	slider.destroy();
});

// Without JQuery
var slider = new Slider("#ex6");
slider.on("slide", function(sliderValue) {
	document.getElementById("ex6SliderVal").textContent = sliderValue;
});

// Without JQuery
var slider = new Slider("#ex7");

$("#ex7-enabled").click(function() {
	if(this.checked) {

		// Without JQuery
		slider.enable();
	}
	else {

		// Without JQuery
		slider.disable();
	}
});

// Without JQuery
var slider = new Slider("#ex8", {
	tooltip: 'always'
});

// Without JQuery
var slider = new Slider("#ex9", {
	precision: 2,
	value: 8.115 // Slider will instantiate showing 8.12 due to specified precision
});

// Without JQuery
var slider = new Slider("#ex10", {});

// Without JQuery
var slider = new Slider("#ex11", {
	step: 20000,
	min: 0,
	max: 200000
});

var sliderA = new Slider("#ex12a", { id: "slider12a", min: 0, max: 10, value: 5 });
var sliderB = new Slider("#ex12b", { id: "slider12b", min: 0, max: 10, range: true, value: [3, 7] });
var sliderC = new Slider("#ex12c", { id: "slider12c", min: 0, max: 10, range: true, value: [3, 7] });

// Without JQuery
var sliderA = new Slider("#ex16a", { min: 0, max: 10, value: 0, focus: true });
var sliderB = new Slider("#ex16b", { min: 0, max: 10, value: [0, 10], focus: true });


// Without JQuery
var sliderA = new Slider("#ex18a", {
	min: 0,
	max: 10,
	value: 5,
	labelledby: 'ex18-label-1'
});
var sliderB = new Slider("#ex18b", {
	min: 0,
	max: 10,
	value: [3, 6],
	labelledby: ['ex18-label-2a', 'ex18-label-2b']
});

// Without JQuery
$("#ex24").slider({});

// Without JQuery
var sliderA = new Slider("#ex17a", {
	min: 0,
	max: 10,
	value: 0,
	tooltip_position:'bottom'
});

var sliderB = new Slider("#ex17b", {
	min: 0,
	max: 10,
	value: 0,
	orientation: 'vertical',
	tooltip_position:'left'
});

$('#ex20a').on('click', function(e) {
      $('#ex20a')
          .parent()
          .find(' >.well')
          .toggle()
          .find('input')
          .slider('relayout');
      e.preventDefault();
  });
  
// Without JQuery
var slider = new Slider("#ex13", {
    ticks: [0, 100, 200, 300, 400],
    ticks_labels: ['$0', '$100', '$200', '$300', '$400'],
    ticks_snap_bounds: 30
});


// Without JQuery
var slider = new Slider("#ex14", {
    ticks: [0, 100, 200, 300, 400],
    ticks_positions: [0, 30, 70, 90, 100],
    ticks_labels: ['$0', '$100', '$200', '$300', '$400'],
    ticks_snap_bounds: 30
});

// Without JQuery
var slider = new Slider('#ex15', {
	min: 1000,
	max: 10000000,
	scale: 'logarithmic',
	step: 10
});