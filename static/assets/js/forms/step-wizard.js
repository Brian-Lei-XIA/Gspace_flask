
$("#example-basic").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	autoFocus: true
});

var form = $("#example-form");
form.validate({
	errorPlacement: function errorPlacement(error, element) { element.after(error); },
	rules: {
		confirm: {
			equalTo: "#password"
		}
	}
});
form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onStepChanging: function (event, currentIndex, newIndex)
	{
		form.validate().settings.ignore = ":disabled,:hidden";
		return form.valid();
	},
	onFinishing: function (event, currentIndex)
	{
		form.validate().settings.ignore = ":disabled";
		return form.valid();
	},
	onFinished: function (event, currentIndex)
	{
		alert("Submitted!");
	}
});

var form1 = $("#vertical-example");
form1.validate({
	errorPlacement: function errorPlacement(error, element) { element.after(error); },
	rules: {
		confirm: {
			equalTo: "#password1"
		}
	}
});
form1.children("div").steps({
	headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    stepsOrientation: "vertical",
	onStepChanging: function (event, currentIndex, newIndex)
	{
		form1.validate().settings.ignore = ":disabled,:hidden";
		return form1.valid();
	},
	onFinishing: function (event, currentIndex)
	{
		form1.validate().settings.ignore = ":disabled";
		return form1.valid();
	},
	onFinished: function (event, currentIndex)
	{
		alert("Submitted!");
	}
});
