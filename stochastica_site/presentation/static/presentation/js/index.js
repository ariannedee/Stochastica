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

  var time = $('.time');

  function setTime(seconds) {
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    if (seconds < 0) {
      $('.timer').text(`0:00`);
    } else if (secs < 10) {
      $('.timer').text(`${mins}:0${secs}`);
    } else {
      $('.timer').text(`${mins}:${secs}`);
    }
  }

  if (time[0]) {
    let seconds = parseInt(time.text());
    seconds -= 1;
    setTime(seconds);

    setInterval(() => {
      seconds -= 1;
      setTime(seconds);
    }, 1000);
  }
});
