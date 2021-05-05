$(document).ready(function () {
	$('#type-basic').on('click',function(){
		swal('Any fool can use a computer')
	});
	
	$('#type-normal').on('click',function(){
		alert('You clicked the button!')
	});
	
	$('#type-withtitle').on('click',function(){
		swal('The Internet?','That thing is still around?','question')
	});
	
	$('#type-withicon').on('click',function(){
		swal({
		  type: 'error',
		  title: 'Oops...',
		  text: 'Something went wrong!',
		  footer: '<a href>Why do I have this issue?</a>'
		})
	});
	
	$('#type-withimage').on('click',function(){
		swal({
			title: 'This is a image.',
			imageUrl: './images/300X375.jpg',
			imageAlt: 'A tall image'
		})
	});
	
	$('#type-success').on('click',function(){
		swal({
			type: 'success',
			title: 'Your work has been saved'
		})
	});
	
	$('#type-info').on('click',function(){
		swal({
			type: 'info',
			title: 'info!'
		})
	});
	
	$('#type-warning').on('click',function(){
		swal({
			type: 'warning',
			title: 'warning!'
		})
	});
	
	$('#type-error').on('click',function(){
		swal({
			type: 'error',
			title: 'error!'
		})
	});
});