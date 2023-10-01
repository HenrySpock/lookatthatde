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
        let listNameDisplay = document.getElementById('listNameDisplay');
        let listNameEdit = document.getElementById('listNameEdit');
        let editButton = document.getElementById('editListNameButton');
        let saveButton = document.getElementById('saveListNameButton');

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

// ****
// Positioning image with arrows.
function swapElements(elm1, elm2) {
  console.log('swap called')
  const parent1 = elm1.parentNode;
  const next1   = elm1.nextSibling === elm2 ? elm1 : elm1.nextSibling;

  // Move `elm1` to right before the position `elm2` was in
  elm2.parentNode.insertBefore(elm1, elm2);

  // Move `elm2` to right before the saved position of `elm1`
  parent1.insertBefore(elm2, next1);
}

document.addEventListener("DOMContentLoaded", function() {
  const imageEntry = document.querySelector('.image-entry');
  const currentUserId = imageEntry.getAttribute('data-current-user-id');
  const listCreatorId = imageEntry.getAttribute('data-creator-id');
  
  const repositionButton = document.getElementById('reposition-btn');

  const editingButtons = document.getElementById('editing-buttons');

  console.log("currentUserId:", currentUserId);
  console.log("listCreatorId:", listCreatorId);

  // if (currentUserId === listCreatorId) {
  //     repositionButton.style.display = ''; // Show the button
  // } else {
  //     repositionButton.style.display = 'none'; // Hide the button
  // }

  if (currentUserId === listCreatorId) {
      editingButtons.style.display = ''; // Show the buttons
  } else {
      editingButtons.style.display = 'none'; // Hide the buttons
  }

  // Initial positions
  let initialPositions = {};

  let images = document.querySelectorAll('img[data-image-id]');
  images.forEach((img, index) => {
    img.setAttribute('data-position', index + 1);
    let imageId = img.getAttribute('data-image-id');
    initialPositions[imageId] = index + 1;
  });

  let arrowsLeft = document.querySelectorAll('.fa-arrow-left');
  let arrowsRight = document.querySelectorAll('.fa-arrow-right');

  arrowsLeft.forEach(arrow => {
      arrow.addEventListener('click', function() {
          console.log("Left arrow clicked"); 
          let imageElement = arrow.parentElement.querySelector('img[data-image-id]');
          console.log('Current Image Element:', imageElement);

          let currentPosition = parseInt(imageElement.getAttribute('data-position'));
          console.log('Current Position:', currentPosition);

          // Additional logic to move the image one place to the right
          let previousImage = document.querySelector(`img[data-position="${currentPosition - 1}"]`);
          console.log('Previous Image:', previousImage);
          if (previousImage) {
              console.log('Attempting to swap with previous image');
              swapElements(imageElement, previousImage);
              previousImage.setAttribute('data-position', currentPosition);
              imageElement.setAttribute('data-position', currentPosition - 1);
          }
      });
  });

  arrowsRight.forEach(arrow => {
      arrow.addEventListener('click', function() {
          console.log("Right arrow clicked");
          let imageElement = arrow.parentElement.querySelector('img[data-image-id]');
          console.log('Current Image Element:', imageElement);

          let currentPosition = parseInt(imageElement.getAttribute('data-position'));
          console.log('Current Position:', currentPosition);

          // Additional logic to move the image one place to the right
          let nextImage = document.querySelector(`img[data-position="${currentPosition + 1}"]`);
          console.log('Next Image:', nextImage);
          if (nextImage) {
              console.log('Attempting to swap with previous image');
              swapElements(nextImage, imageElement);
              nextImage.setAttribute('data-position', currentPosition);
              imageElement.setAttribute('data-position', currentPosition + 1);
          }
      });
  });

  let saveButton = document.getElementById('save-btn');
  saveButton.addEventListener('click', function() {
      let updatedImagePositions = {};

      images.forEach(img => {
          let imageId = img.getAttribute('data-image-id');
          let position = img.getAttribute('data-position');

          if (initialPositions[imageId] !== position) {
              updatedImagePositions[imageId] = position;
          }
      });

      if (Object.keys(updatedImagePositions).length === 0) {
          alert('No changes detected.');
          return;
      }

      let csrfToken = document.querySelector('input[name="csrf_token"]').value;

      fetch('/images/update_image_positions', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrfToken
          },
          body: JSON.stringify(updatedImagePositions),
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Image positions updated successfully!');
          } else {
              alert('Error updating image positions: ' + data.error);
          }
      })
      .catch((error) => {
          console.error('Error:', error);
      });
  });

  // let repositionButton = document.getElementById('reposition-btn');
  // let saveButton = document.getElementById('save-btn');
  // let arrows = document.querySelectorAll('.image-arrow');
  let arrows = document.querySelectorAll('.reposition-arrow');
  // Click event for "Reposition images?" button
  // repositionButton.addEventListener('click', function() {
  //     // Hide "Reposition images?" button
  //     repositionButton.style.display = 'none';
      
  //     // Show arrows
  //     arrows.forEach(arrow => {
  //         arrow.style.display = '';
  //     });

  //     // Show "Save Position?" button
  //     saveButton.style.display = '';
  // });

  repositionButton.addEventListener('click', function() {
    // Hide "Reposition images?" button
    repositionButton.style.display = 'none';
    
    let images = document.querySelectorAll('.image-entry');

    // Loop through all the image entries and decide which arrows to show
    images.forEach((entry, index) => {
        let leftArrow = entry.querySelector('.fa-arrow-left');
        let rightArrow = entry.querySelector('.fa-arrow-right');

        if (index === 0) {  // First image entry
            leftArrow.style.display = 'none';
            rightArrow.style.display = '';
        } else if (index === images.length - 1) {  // Last image entry
            leftArrow.style.display = '';
            rightArrow.style.display = 'none';
        } else {  // All other image entries
            leftArrow.style.display = '';
            rightArrow.style.display = '';
        }
    });

    // Show "Save Position?" button
    saveButton.style.display = '';
});

  // Modify your existing saveButton event listener
  saveButton.addEventListener('click', function() {
      
      // ... [rest of your saving logic] ...

      // Once saving is done:
      
      // Hide arrows
      arrows.forEach(arrow => {
          arrow.style.display = 'none';
      });

      // Hide "Save Position?" button
      saveButton.style.display = 'none';

      // Show "Reposition images?" button
      repositionButton.style.display = '';
  });

});
