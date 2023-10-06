 // An array holding the paths to background images.
 const backgroundImages = [
  '/static/images/latbg1.jpg',
  '/static/images/latbg2.jpg',
  '/static/images/latbg3.jpg', 
  '/static/images/latbg4.jpg', 
  '/static/images/latbg5.jpg', 
  '/static/images/latbg6.jpg', 
  '/static/images/latbg7.jpg', 
  '/static/images/latbg8.jpg', 
  '/static/images/latbg9.jpg', 
  '/static/images/latbg10.jpg', 
  '/static/images/latbg11.jpg', 
  '/static/images/latbg12.jpg', 
  '/static/images/latbg13.jpg', 
  '/static/images/latbg14.jpg', 
  '/static/images/latbg15.jpg', 
  '/static/images/latbg16.jpg', 
  '/static/images/latbg17.jpg', 
  '/static/images/latbg18.jpg', 
  '/static/images/latbg19.jpg', 
  '/static/images/latbg20.jpg', 
  '/static/images/latbg21.jpg', 
  '/static/images/latbg22.jpg', 
  '/static/images/latbg23.jpg', 
];

// Event listener to execute when the document is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
  // Randomly select an image path from the `backgroundImages` array.
  const randomImage = backgroundImages[Math.floor(Math.random() * backgroundImages.length)];
  // Apply the randomly selected image as a background to the element with class `main-content`.
  document.querySelector('.main-content').style.setProperty('--random-bg', `url('${randomImage}')`);
});

 

 
 