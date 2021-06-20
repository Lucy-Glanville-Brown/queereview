
var exampleModal = document.getElementById('exampleModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var comment_id = button.getAttribute('data-bs-whatever')
 
//   comment_id = "ObjectId('"+ comment_id + "')"
//   document.getElementById('delete-comment-form').action = "{{ url_for('delete_comment', post=post._id, comment_id="+ comment_id+"))}}";
})

