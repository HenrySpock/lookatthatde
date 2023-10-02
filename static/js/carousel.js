// Variables to control the slideshow
var slideIndex = 0;
var slideInterval;
var slides = document.getElementsByClassName("mySlides");

// Function to show the slides
function showSlides() {
  console.log("showSlides triggered");
  for (var i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  if (slideIndex >= slides.length) {
      slideIndex = 0; // Reset to the first slide
  }

  slides[slideIndex].style.display = "block";
  slideIndex++;
}

// Function to start the slideshow
function startSlideshow() { 
    console.log("Starting the slideshow.");
    slideInterval = setInterval(showSlides, 2000); // Change slide every 2 seconds
}

// Only run on the /slideshow/<id> page.
// Adjust the condition as needed based on your URL structure.
if (window.location.pathname.includes("/slideshow/")) {
  document.addEventListener("DOMContentLoaded", function() {
    startSlideshow();
  });
}


