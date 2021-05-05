$(document).ready(function(){
	var callbacks_list = $('.demo-callbacks ul');
	$('.demo-list input').on('ifCreated ifClicked ifChanged ifChecked ifUnchecked ifDisabled ifEnabled ifDestroyed', function(event){
		callbacks_list.prepend('<li><span>#' + this.id + '</span> is ' + event.type.replace('if', '').toLowerCase() + '</li>');
	}).iCheck({
		checkboxClass: 'icheckbox_square-blue',
		radioClass: 'iradio_square-blue',
		increaseArea: '20%'
	});
});

$(document).ready(function(){
  $('.skin-minimal input').iCheck({
	checkboxClass: 'icheckbox_minimal',
	radioClass: 'iradio_minimal',
	increaseArea: '20%'
  });
});

$(document).ready(function(){
  $('.skin-square input').iCheck({
	checkboxClass: 'icheckbox_square-green',
	radioClass: 'iradio_square-green',
	increaseArea: '20%'
  });
});

$(document).ready(function(){
  $('.skin-flat input').iCheck({
	checkboxClass: 'icheckbox_flat-red',
	radioClass: 'iradio_flat-red'
  });
});

$(document).ready(function(){
  $('.skin-line input').each(function(){
	var self = $(this),
	  label = self.next(),
	  label_text = label.text();

	label.remove();
	self.iCheck({
	  checkboxClass: 'icheckbox_line-blue',
	  radioClass: 'iradio_line-blue',
	  insert: '<div class="icheck_line-icon"></div>' + label_text
	});
  });
});

$(document).ready(function(){
  $('.skin-polaris input').iCheck({
	checkboxClass: 'icheckbox_polaris',
	radioClass: 'iradio_polaris',
	increaseArea: '-10%'
  });
});

$(document).ready(function(){
  $('.skin-futurico input').iCheck({
	checkboxClass: 'icheckbox_futurico',
	radioClass: 'iradio_futurico',
	increaseArea: '20%'
  });
});