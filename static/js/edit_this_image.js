// Handle 'Edit This Image' button 
document.querySelectorAll('.editImageButton').forEach(function(button) {
  button.addEventListener('click', function() {
    let listId = this.getAttribute('data-list-id');
    let imageId = this.getAttribute('data-image-id');
    let imageUrl = this.getAttribute('data-image-url');
    let url = '/images/edit_image/' + listId + '/' + imageId + '?selected_image_url=' + imageUrl;
    console.log("Button clicked. Redirecting to:", url);
    window.location.href = url;
  });
});