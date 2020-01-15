var a = document.getElementById('new-post')
var func = function() {
  // text box
  var div = document.createElement("div");
  div.className = "form-horizontal"
  div.innerHTML = `
    <div class="form-group">
        <div class="col-md-6">
            <textarea class="form-control" rows="3" placeholder="What's up?" name="body" required></textarea>
        </div>
    </div>
  `;
  document.getElementById("feed").appendChild(div);

  var button = document.createElement("a");
  button.type = "button";
  button.className = "btn btn-success ml-3";
  button.innerHTML = "Post!";
  button.href = "/posting";
  document.getElementById("feed").appendChild(button);
  /*var thing = document.createElement("div");
  thing.innerText = "Hello World";
  document.getElementById("feed").appendChild(thing);*/
}
a.addEventListener('click', func);

function newElement() {
  var li = document.createElement("li");
  var inputValue = document.getElementById("myInput").value;
  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue === '') {
    alert("You must write something!");
  } else {
    document.getElementById("myUL").appendChild(li);
  }
  document.getElementById("myInput").value = "";

  var span = document.createElement("SPAN");
  //var txt = document.createTextNode("\u00D7");
  span.className = "close";
  //span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      div.style.display = "none";
    }
  }
}
