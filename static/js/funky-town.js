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
