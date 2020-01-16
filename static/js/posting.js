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

}
a.addEventListener('click', func);
