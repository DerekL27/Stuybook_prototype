var a = document.getElementById('new-post')
var func = function() {
  // text box
  var div = document.createElement("div");
  div.className = "form-horizontal"
  div.innerHTML = `
    <form action='/posting' method='POST'>
    <div class="form-group" id="salad">
        <div class="col-md-6">
            <textarea class="form-control" rows="3" placeholder="What's up?" name="hello" required></textarea>
        </div>
    </div>
    </form>
  `;
  document.getElementById("feed").appendChild(div);

  var button = document.createElement("a");
  button.type = "submit";
  button.className = "btn btn-success ml-3";
  button.innerHTML = "Post!";
  document.getElementById("salad").appendChild(button);
  /*var thing = document.createElement("div");
  thing.innerText = "Hello World";
  document.getElementById("feed").appendChild(thing);*/
}
a.addEventListener('click', func);
