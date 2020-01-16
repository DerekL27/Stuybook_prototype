var bro = document.getElementById('editbio')
var another = function() {
  console.log('yes');
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
    <button type="submit" class="btn btn-warning ml-3">Save</button><br><br>
    </form>
  `;
  //document.getElementById("editbox").appendChild(div);
}
bro.addEventListener('click', another);
