// Handle 'Edit List Name' button 
function editListName() {
    const editButton = document.getElementById('editListNameButton');
    const editUrl = editButton.getAttribute('data-edit-url');
    window.location.href = editUrl;
}

// Handle 'Edit Fields' button 
document.getElementById('editFieldsButton').addEventListener('click', function() {
    let listId = this.getAttribute('data-list-id');
    console.log('list id for edit fields: ', listId);
    let url = '/lists/edit_fields_get/' + listId;
    console.log("Redirecting to:", url);
    window.location.href = url;
  });

// **************************
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

  const showHideEdit = document.getElementsByClassName('show-hide-edit');

  console.log("currentUserId:", currentUserId);
  console.log("listCreatorId:", listCreatorId);

  // Loop through each button in the collection
  for(let button of showHideEdit) {
      if (currentUserId === listCreatorId) {
          button.style.display = ''; // Show the button
      } else {
          button.style.display = 'none'; // Hide the button
      }
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

          // Additional logic to move the image one place to the left
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
              console.log('Attempting to swap with next image');
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

    //   let csrfToken = document.querySelector('input[name="csrf_token"]').value;
      const csrfToken = document.getElementById("csrfToken").value;

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

  let arrows = document.querySelectorAll('.reposition-arrow'); 

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

function toggleCategory(listId) {
    const csrfToken = document.getElementById("csrfToken").value;
    const button = document.getElementById("categoryButton");
    const addCategoryUrl = button.getAttribute("data-add-url");

    if (button.innerText === "Remove Category?") {
        fetch(`/lists/remove_category/${listId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                // Change button to 'Add a Category?'
                button.innerText = 'Add a Category?';
                button.onclick = function() { location.href = addCategoryUrl; };
                showToast(data.message);
            } else { 
                showToast("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error.message);
        });
    } else {
        // If the button says 'Add a Category?', redirect to the add category page.
        location.href = addCategoryUrl;
    }
}
 
// Function to show the toast
function showToast(message) {
    const toast = document.getElementById("liveToast");
    const toastBody = toast.querySelector(".toast-body");

    // Set the toast message
    toastBody.textContent = message;

    // Show the toast by adding the "show" class
    toast.classList.add("show");

    // Check if the toast is displayed
    if (toast.classList.contains("show")) {
        // Add padding to the toast-body when it's displayed
        toastBody.style.padding = "15px";
    }

    // Automatically hide the toast after a certain time
    setTimeout(function () {
        hideToast();
    }, 5000); // Adjust the time as needed
}

// Function to hide the toast
function hideToast() {
    const toast = document.getElementById("liveToast");

    // Hide the toast by removing the "show" class
    toast.classList.remove("show");
}


// Going to the carousel
// JavaScript function to navigate to the carousel page with list_id
function goToCarousel(list_id) {
    const url = `/lists/carousel/${list_id}`; // Construct the URL
    window.location.href = url; // Redirect to the carousel page
}

// Add a click event listener to the slideshow button
const slideshowButton = document.getElementById('slideshow-button');
slideshowButton.addEventListener('click', function() {
    const list_id = this.getAttribute('data-list-id');
    goToCarousel(list_id); // Call the function with the list_id
});

// Handle Add Image button:
function redirectTo(url) {
    window.location.href = url;
}



let areFieldsHidden = false;
function toggleFields() {
    console.log("Toggle fields function triggered");
    const button = document.getElementById('toggleFieldsButton');
    const fields = document.querySelectorAll('.card-fields');

    if (areFieldsHidden) {
        fields.forEach(field => field.style.display = '');
        button.textContent = "Hide Fields";
        areFieldsHidden = false;
    } else {
        fields.forEach(field => field.style.display = 'none');
        button.textContent = "Show Fields";
        areFieldsHidden = true;
    }
}

