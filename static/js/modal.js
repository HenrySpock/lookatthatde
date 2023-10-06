// Get the modal
let modal = document.getElementById('imageNameModal');

// When the user clicks on <span> (x), close the modal
let span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    modal.style.display = "none";
}

// This function is to open the modal
function openImageNameModal() {
    modal.style.display = "block";
}

// This function will handle saving the image URL with the given name
function saveImageUrlWithName(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    let imageUrl = document.getElementById('manualImageUrl').value;
    let imageName = document.getElementById('imageName').value;
    let csrfToken = document.querySelector("input[name='csrf_token']").value; 
    let listId = document.getElementById('list_id').value;

    fetch('/images/save_image/' + listId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            imageUrl: imageUrl,
            imageName: imageName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/lists/list_details/" + listId; // Redirect to another page (if needed)
        } else {
            alert("Error saving the image.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function chooseImage(imageUrl, listId) { 
  console.log(imageUrl, listId);
  
  // Open the modal
  document.getElementById('imageNameModal').style.display = "block";
}

function chooseImageFromList(imageUrl, listId) {
  // Open the modal
  openImageNameModal();

  // Save the imageUrl to a global variable or a hidden input field so we can access it later
  document.getElementById('selectedImageUrl').value = imageUrl;
}

function saveSelectedImageUrlWithName(event) {
  event.preventDefault();

  console.log("Inside the saveSelectedImageUrlWithName function");
  console.log(document.getElementById('selectedImageUrl'));
  console.log("Value of selectedImageUrl:", document.getElementById('selectedImageUrl').value);

  let imageUrl = document.getElementById('selectedImageUrl').value;
  let imageName = document.getElementById('imageName').value;
  let listId = document.getElementById('list_id').value;
  console.log('imageUrl: ', imageUrl, 'imageName: ', imageName, 'listId: ', listId);

  if(!imageUrl || !imageName || !listId) {
    console.error("Missing data: ", { imageUrl, imageName, listId });
    return;
  }

  console.log('CSRF token: ', document.getElementById('csrf_token').value);
  let csrfToken = document.querySelector("input[name='csrf_token']").value;
  console.log("Fetched CSRF Token:", csrfToken);
  fetch('/images/save_image/' + listId, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.getElementById('csrf_token').value
      },
      body: JSON.stringify({
          imageUrl: imageUrl,
          imageName: imageName
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          window.location.href = "/lists/list_details/" + listId;
      } else {
          alert("Error saving the image.");
      }
  })
  .catch(error => {
      console.error("Error:", error);
  });
}
