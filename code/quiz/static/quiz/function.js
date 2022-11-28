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

function to_url_new_page(url){
  window.open(url);
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
      t=t+"<li><button onclick='show_question("+(i+1)+")' style='' id='problem"+(i+1)+"' type='button' class ='buttons' >Problem"+(i+1)+"</button></li>"
    }
    return t;
  }
  
}

function add(id){
  var divBox = document.getElementById('mydiv'+id);
  var newdiv = document.createElement('div');
  number  = divBox.childElementCount-5;
  newdiv.class='image_and_preview';
  newdiv.style='margin-top:20px';
  newdiv.id = number+"image_and_preview"+id;
  newdiv.innerHTML="<img id ='"+number+"imgPreview"+id+"'  width='0' height='0'/> <input type='file' id='"+number+'_'+id+"' name='"+number+"img' accept='image/gif, image/jpeg, image/png, image/jpg' onchange='preview(100,100,"+number+","+id+")' > <a ></a>";
  divBox.appendChild(newdiv);
}




function del(id){
  var divBox = document.getElementById('mydiv'+id);
  number  = divBox.childElementCount-5;

  if (number!=0) number--;
  else{
    var bu = document.getElementById('addimg'+id);
    bu.style.display='inline';
    divBox.style.display='none';
  }
  var x = document.getElementById(number+'image_and_preview'+id);
  x.parentNode.removeChild(x);
}

function preview(width, height,number,id){
  var x = document.getElementById(number+'_'+id);

  var name = x.files[0];
  if (window.URL != undefined && name){
      url = window.URL.createObjectURL(name);
  }
  var z = url;
  var y = document.getElementById(number+'imgPreview'+id);
  
  if (x.value=="") {y.src="";y.width=0;y.height=0}
  else{y.width=width;y.height=height;y.src=z;}
}

function assign_size_img(img_tags){
  for (var i =0; i < img_tags.length;i++){
    var img = img_tags[i];
    if (img.parentElement.parentElement.parentElement.className=='comment'){
      img.style='max-height:300px;max-width:90%';
    }
    else if (img.parentElement.parentElement.parentElement.className=='reply'){
      img.style='max-height:200px;max-width:80%';
    }
  }
}

function show_img(id,this_id){
  var x = document.getElementById(id);
  x.style.display='inline';
  document.getElementById(this_id).style.display='none';
}

function change_mult_value(answer_str,dict_str){
  answer_str=answer_str.replaceAll(" ","") // Drop all the spaces
  var answer = ""
  for(var i = 0 ; i< answer_str.length;i++){
    var char = answer_str.charAt(i)
    var charcode = char.charCodeAt(0)-97;
    if (charcode > dict_str.length-1){
      return ""
    }
    answer +=dict_str.charAt(char.charCodeAt(0)-97)+" "
  }
  return answer;
}