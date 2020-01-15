var a = document.getElementById('new-post')
var func = function() {
  // text box
  var div = document.createElement("div");
  div.className = "form-horizontal"
  div.innerHTML = `
    <form action='/posting' method='POST'>
    <div class="form-group" id="salad">
        <div class="col-md-6">
            <textarea class="form-control" rows="3" placeholder="What's up?" name="body" required></textarea>
        </div>
    </div>
    <button type="submit" class="btn btn-success ml-3">Post!</button>
    </form>
  `;
  document.getElementById("makepost").appendChild(div);

  /*var thing = document.createElement("div");
  thing.innerText = "Hello World";
  document.getElementById("feed").appendChild(thing);*/
}
a.addEventListener('click', func);

var bro = document.getElementById('editbio')
var another = function() {
  var div = document.createElement("div");
  div.className = "form-horizontal"
  var place = document.getElementById('currentbio').innerHTML
  div.innerHTML = `
    <form action='/edit_bio' method='POST'>
    <div class="form-group">
        <div class="col-md-10">
            <textarea class="form-control" rows="3" placeholder="Something new" name="newbio" required></textarea>
        </div>
    </div>
    <button type="submit" class="btn btn-warning ml-3">Save</button>
    </form>
  `;
  document.getElementById("editbox").appendChild(div);
}
bro.addEventListener('click', another);
