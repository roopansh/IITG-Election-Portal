function getTimeRemaining(endtime){
  var seconds = endtime;
  /*var minutes = Math.floor( (endtime/60));*/
  return {
    'total': endtime,
    'seconds': seconds
  };
};

window.onload = function (){
  var clock = document.getElementById("clockdiv");
  var timeinterval = setInterval(function(){
    var t = getTimeRemaining(clock.innerHTML);
    clock.innerHTML = t.seconds - 1;
    if(t.total<=1){
      alert("Your time is up!");
      clearInterval(timeinterval);
      window.location = "/vote/logout/";
    }
  },1000);
};