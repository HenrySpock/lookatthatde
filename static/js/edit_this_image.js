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