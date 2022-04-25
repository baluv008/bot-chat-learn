function func(){
    var x = document.getElementById("chatterbox");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}
function send_chat()
{

  chat_text = document.getElementById("textInput").value;
  document.getElementById("textInput").value = ""
  var today = new Date();

    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

  new_div = '<div class="container"><p class="message user">'+chat_text+'<br><span class="time-right">'+time+'</span></p><br></div><br>'
  var element = document.getElementById("chatcontent");
  element.scrollTop = element.scrollHeight;
  $("#chatcontent").append(new_div)
  $.ajax({
        url:"/chat",
        type:"POST",
        data:{"chat_msg":chat_text},
        async:true,
        success:function(response)
        {

            var today = new Date();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            new_div = '<div class="container"><p class="message bot">'+response+'<br><span class="time-left">'+time+'</span></p></div><br><br>'
            $("#chatcontent").append(new_div)
            var element = document.getElementById("chatcontent");
            element.scrollTop = element.scrollHeight;
        }
      });
}
