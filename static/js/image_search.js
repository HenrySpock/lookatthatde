// console.log("Script Loaded")

// document.addEventListener('DOMContentLoaded', function() {
//   console.log("DOMContentLoaded fired");

//   // Fetch list_id from the hidden input field
//   const listId = document.getElementById('listId').value;

//   // Search form functionality
//   document.getElementById('searchForm').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const query = document.getElementById('searchQuery').value;
//     window.location.href = `/images/image_response?search_query=${query}`;
//   });

//   // Manual input form functionality
//   document.getElementById('manualInputForm').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const imageUrl = document.getElementById('manualImageUrl').value;

//     // Check if the imageUrl is not empty
//     if (!imageUrl.trim()) {
//         alert("Please enter a valid URL.");
//         return;
//     }

//     // Simple regex pattern check for URLs
//     const pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
//     if (!pattern.test(imageUrl)) {
//         alert("Please enter a valid URL.");
//         return;
//     }

//     // Redirect to the image_response view with the manually inputted URL
//     window.location.href = `/images/image_response?manual_image_url=${encodeURIComponent(imageUrl)}`;
//   });

// });

console.log("Script Loaded");
// alert("List ID: " + list_id);

document.addEventListener('DOMContentLoaded', function() {
  console.log("DOMContentLoaded fired");

  // Fetch list_id from the hidden input field
  const list_id = document.getElementById('list_id').value;  
  console.log('from image_search.js, list_id: ', list_id)

  // Search form functionality
  document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;
    window.location.href = `/images/image_response/${list_id}?search_query=${query}`;
  });

  // Manual input form functionality
  document.getElementById('manualInputForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const imageUrl = document.getElementById('manualImageUrl').value;

    // // Check if the imageUrl is not empty
    // if (!imageUrl.trim()) {
    //     alert("Please enter a valid URL.");
    //     return;
    // }

    // // Simple regex pattern check for URLs
    // const pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    // if (!pattern.test(imageUrl)) {
    //     alert("Please enter a valid URL.");
    //     return;
    // }

    // Check if the imageUrl is not empty
    if (!imageUrl.trim()) {
      window.location.href = `/images/image_search/${list_id}?error=empty_url`;
      return;
    }

    // Simple regex pattern check for URLs
    const pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    if (!pattern.test(imageUrl)) {
      window.location.href = `/images/image_search/${list_id}?error=invalid_url`;
      return;
    }

    // Redirect to the image_response view with the manually inputted URL
    window.location.href = `/images/image_response/${list_id}?manual_image_url=${encodeURIComponent(imageUrl)}`;
  });

});
