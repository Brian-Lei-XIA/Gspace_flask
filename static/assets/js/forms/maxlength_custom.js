$('.form-control').maxlength({
	placement: 'bottom',
	warningClass: "badge badge-danger",
	limitReachedClass: "badge badge-success",
	alwaysShow: true,
	validate: false,
	allowOverMax: true,
    customMaxAttribute: "90"
});

$('.form-control.threshold').maxlength({
	placement: 'bottom',
	warningClass: "badge badge-danger",
	limitReachedClass: "badge badge-success",
	alwaysShow: true,
	validate: false,
	allowOverMax: true,
	threshold: 20,
    customMaxAttribute: "90"
});

$('#max_textarea').maxlength({
	placement: 'bottom',
	warningClass: "badge badge-danger",
	limitReachedClass: "badge badge-success",
	alwaysShow: true,
	validate: false,
	allowOverMax: true,
    customMaxAttribute: "90"
});