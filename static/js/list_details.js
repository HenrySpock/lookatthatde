document.getElementById('editFieldsButton').addEventListener('click', function() {
  var listId = this.getAttribute('data-list-id');
  window.location.href = '/images/edit_fields/' + listId;
});