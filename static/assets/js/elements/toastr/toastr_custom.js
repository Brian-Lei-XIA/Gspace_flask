$(document).ready(function(){

	// Success Type
	$('#type-success').on('click',function(){
		toastr.success('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	// Success Type
	$('#type-info').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	// Success Type
	$('#type-warning').on('click',function(){
		toastr.warning('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	// Success Type
	$('#type-error').on('click',function(){
		toastr.error('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	// Position Top Left
	$('#position-top-left').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Top Left!', {positionClass: 'toast-top-left'});
	});

	// Position Top Center
	$('#position-top-center').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Top Center!', {positionClass: 'toast-top-center'});
	});

	// Position Top Right
	$('#position-top-right').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Top Right!', {positionClass: 'toast-top-right'});
	});

	// Position Top Full Width
	$('#position-top-full').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Top Full Width!', {positionClass: 'toast-top-full-width'});
	});

	// Position Bottom Left
	$('#position-bottom-left').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Bottom Left!', {positionClass: 'toast-bottom-left'});
	});

	// Position Bottom Center
	$('#position-bottom-center').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Bottom Center!', {positionClass: 'toast-bottom-center'});
	});

	// Position Bottom Right
	$('#position-bottom-right').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Bottom Right!', {positionClass: 'toast-bottom-right'});
	});

	// Position Bottom Full Width
	$('#position-bottom-full').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Bottom Full Width!', {positionClass: 'toast-bottom-full-width'});
	});

	// Text Notification
	$('#text-notification').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Miracle Max Says');
	});

	// Close Button
	$('#close-button').on('click',function(){
		toastr.success('We do have the Kapua suite available.', 'With Close Button', {"closeButton": true});
	});

	// Progress Bar
	$('#progress-bar').on('click',function(){
		toastr.warning('We do have the Kapua suite available.', 'Progress Bar', {"progressBar": true});
	});

	// Clear Toast Button
	$('#clear-toast-btn').on('click',function(){
		toastr.error('Clear itself?<br /><br /><button type="button" class="btn btn-secondary clear">Yes</button>', 'Clear Toast Button');
	});


	// Immediately remove current toasts without using animation
	$('#show-remove-toast').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	$('#remove-toast').on('click',function(){
		toastr.remove();
	});

	// Remove current toasts using animation
	$('#show-clear-toast').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Turtle Bay Resort');
	});

	$('#clear-toast').on('click',function(){
		toastr.clear();
	});


	// Fast Duration
	$('#fast-duration').on('click',function(){
		toastr.success('We do have the Kapua suite available.', 'Fast Duration', {"showDuration": 500});
	});

	// Slow Duration
	$('#slow-duration').on('click',function(){
		toastr.warning('We do have the Kapua suite available.', 'Slow Duration', {"hideDuration": 3000});
	});

	// Timeout
	$('#timeout').on('click',function(){
		toastr.error('We do have the Kapua suite available.', 'Timeout!', {"timeOut": 5000});
	});

	// Sticky
	$('#sticky').on('click',function(){
		toastr.info('We do have the Kapua suite available.', 'Sticky!', {"timeOut": 0});
	});

	// Slide Down / Slide Up
	$('#slide-toast').on('click',function(){
		toastr.success('We do have the Kapua suite available.', 'Slide Down / Slide Up!', {"showMethod": "slideDown", "hideMethod": "slideUp", timeOut: 2000});
	});

	// Fade In / Fade Out
	$('#fade-toast').on('click',function(){
		toastr.success('We do have the Kapua suite available.', 'Slide Down / Slide Up!', {"showMethod": "fadeIn", "hideMethod": "fadeOut", timeOut: 2000});
	});
});