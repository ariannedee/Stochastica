$(document).ready(()=> {
const LEFT_ARROW = 37;
const RIGHT_ARROW = 39;
const SPACE = 32;
$(document).keydown(function(event){

	var keycode = (event.keyCode ? event.keyCode : event.which);
	if(keycode == LEFT_ARROW){
		$('#back')[0].click();
	}
	if(keycode == RIGHT_ARROW | keycode == SPACE){
		$('#next')[0].click();
	}
});
});
