// document.addEventListener('DOMContentLoaded', function() {
//   const buttons = document.querySelectorAll('.select-image-btn');
//   buttons.forEach(btn => {
//       btn.addEventListener('click', function() {
//           const imageUrl = this.getAttribute('data-image-url');
//           window.location.href = `/images/edit_image/${list_id}?selected_image_url=${encodeURIComponent(imageUrl)}`;
//       });
//   });
// });

function chooseImage(imageUrl, list_id) {
  // Add a confirmation popup
  if (confirm("You can change this image later if you wish. Proceed?")) {
      window.location.href = `/images/edit_image/${list_id}?selected_image_url=${encodeURIComponent(imageUrl)}`;
  }
}
