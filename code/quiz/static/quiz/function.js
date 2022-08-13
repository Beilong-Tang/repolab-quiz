// Log out confirmation
function confirmation(y){
    var x = confirm("Are you sure you want to log out?");
    if (x == true){
      window.location.href=y}
  }

// Forum Page
function to_url(url){
  window.location.href = url;
  return
}

// forum post page
function to_forum_post(id,url,length){
  url = url.replace('1:',''+id+':').replace(':0',':'+length);
  window.location.href = url;
  return;
}


// function to change img color
const colors = ['#00AA55', '#009FD4', '#B381B3', '#939393', '#E3BC00', '#D47500', '#DC2A2A', 'rgb(202,62,94)', "#50EBEC" , "#FFDAB9", "#F67280", "#307D7E"];

function numberFromText(text) {
// numberFromText("AA");
const charCodes = text
    .split(' ') // => ["A", "A"]
    .map(char => char.charCodeAt(0)) // => [65, 65]
    .join(''); // => "6565"
var num =  parseInt(charCodes, 10);
return colors[num % colors.length]

}

function open_chat_room(){
  var x = document.getElementById('chat_room');
  x.style.display="inline";

}

function close_chat_room(){
  var x = document.getElementById('chat_room');
  x.style.display="none";

}

function select(y,week1,week2,week3,week4,week5,week6,week7){
  
  if (y==1){
    var z = parseInt(week1);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>";
    }
    return t;
  }
  if (y==2){
    var z = parseInt(week2);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  if (y==3){
    var z = parseInt(week3);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  if (y==4){
    var z = parseInt(week4);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  if (y==5){
    var z = parseInt(week5);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  if (y==6){
    var z = parseInt(week6);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  if (y==7){
    var z = parseInt(week7);
    var t = "";
    for( var i = 0 ; i <z ; i++){
      t=t+"<li><button onclick='show_question()' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  
}