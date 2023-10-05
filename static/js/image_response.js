function chooseImage(imageUrl, list_id) {
  // Add a confirmation popup
  if (confirm("You can change this image later if you wish. Proceed?")) {
      window.location.href = `/images/edit_image/${list_id}?selected_image_url=${encodeURIComponent(imageUrl)}`;
  }
}
