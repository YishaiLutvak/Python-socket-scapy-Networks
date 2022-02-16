var left = 0, down = 0;

function moveLeftTimeout(){
  setTimeout(function(){
    if(left<300){
      left++
      document.getElementById("box").style.left = left +"px";
      if (left % 300 > down + 1) {
        document.getElementById("box").innerHTML = "Run</br>Away"  
      } else {
        document.getElementById("box").innerHTML = "Why</br>Ahhh"
      }
      
      moveLeftTimeout();
    } else {
      left = 0, down = 0;
       document.getElementById("box").style.left = "0px";
       document.getElementById("box").style.top = "0px";
       document.getElementById("box").innerHTML = ""
    }
  },15);
}

function moveDownInterval(){
  var theTimer = setInterval(function(){
    if(down<250){
        down++
        //console.log(document.getElementById("box").style);
        document.getElementById("box").style.top = down +"px";
      }
    else{ clearInterval(theTimer); }
  },15);
  } 

box = document.getElementById("box");
box.addEventListener("click",  function(){
  moveLeftTimeout();
  moveDownInterval();
})