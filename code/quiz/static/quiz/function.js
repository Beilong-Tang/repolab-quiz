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
