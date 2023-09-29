// Handle 'Edit Fields' button 
document.getElementById('editFieldsButton').addEventListener('click', function() {
  var listId = this.getAttribute('data-list-id');
  var url = '/images/edit_fields/' + listId;
  console.log("Redirecting to:", url);
  window.location.href = url;
});

// Handle 'Edit This Image' button 
document.querySelectorAll('.editImageButton').forEach(function(button) {
  button.addEventListener('click', function() {
    var listId = this.getAttribute('data-list-id');
    var imageId = this.getAttribute('data-image-id');
    var imageUrl = this.getAttribute('data-image-url');
    var url = '/images/edit_image/' + listId + '/' + imageId + '?selected_image_url=' + imageUrl;
    console.log("Button clicked. Redirecting to:", url);
    window.location.href = url;
  });
});

// Handle "Add a category?" button 
function showCategoryForm() {
  const formDiv = document.getElementById("categoryForm");
  formDiv.style.display = "block";
}

// Update List Name  
    function toggleListNameEdit() {
        var listNameDisplay = document.getElementById('listNameDisplay');
        var listNameEdit = document.getElementById('listNameEdit');
        var editButton = document.getElementById('editListNameButton');
        var saveButton = document.getElementById('saveListNameButton');

        listNameDisplay.style.display = 'none';
        listNameEdit.style.display = 'block';
        editButton.style.display = 'none';
        saveButton.style.display = 'block';
    }

function saveListName() {
  console.log('Editing')
  var listNameEdit = document.getElementById('listNameEdit');
  var newName = listNameEdit.value;
  var form = document.getElementById('updateListNameForm'); // Add an ID to the form

  // Set the input field value to the new name
  form.querySelector('input[name="new_name"]').value = newName;

  // Submit the form via AJAX
  fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Update the displayed name on the page
          document.getElementById('listNameDisplay').innerText = newName;
          document.getElementById('listNameDisplay').style.display = 'block';

          // Hide the input field and "Save List Name" button
          listNameEdit.style.display = 'none';
          document.getElementById('saveListNameButton').style.display = 'none';

          // Show the "Edit List Name" button
          document.getElementById('editListNameButton').style.display = 'block';
      } else {
          // Handle any error here, maybe display a message to the user.
          console.error("Failed to update the list name.");
      }
  })
  .catch(error => {
      // This catch block will handle any error thrown in the above then blocks.
      console.error("An error occurred:", error.message);
  });
}



