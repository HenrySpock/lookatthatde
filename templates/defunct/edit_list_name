// function editListName() {
//     const editButton = document.getElementById('editListNameButton');
//     const editUrl = editButton.getAttribute('data-edit-url');
//     window.location.href = editUrl;
// }

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById('saveListNameButton').addEventListener('click', function(e) {
      e.preventDefault(); // Prevent the default form submission
      
      const form = e.target.closest('form');
      const newName = document.getElementById('listName').value;
      
      // Retrieve the CSRF token value from the HTML element
      const csrfToken = form.querySelector('input[name="csrf_token"]').value;

      // Submit the form via AJAX
      fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 
              'X-CSRFToken': csrfToken
          },
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              const listId = e.target.getAttribute('data-list-id');
              window.location.href = `/lists/list_details/${listId}`;
          } else {
              console.error("Failed to update the list name.");
          }
      })
      .catch(error => {
          console.error("An error occurred:", error.message);
      });
  });
});

document.getElementById('cancelButton').addEventListener('click', function() {
    const listId = document.getElementById('saveListNameButton').getAttribute('data-list-id');
    window.location.href = `/lists/list_details/${listId}`;
});