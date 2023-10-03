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
// function startSlideshow() { 
//     console.log("Starting the slideshow.");
//     slideInterval = setInterval(showSlides, 2000); // Change slide every 2 seconds
// }

// Function to start the slideshow
function startSlideshow() { 
  toggleNavbar()
  document.body.classList.add('slideshow-active');
  slideInterval = setInterval(showSlides, 2000); // Change slide every 2 seconds
}

// Only run on the /slideshow/<id> page.
// Adjust the condition as needed based on your URL structure.
if (window.location.pathname.includes("/slideshow/")) {
  document.addEventListener("DOMContentLoaded", function() {
    startSlideshow();
  });
}

// document.body.addEventListener('click', function() {
//   console.log("Body clicked!");
//   clearInterval(slideInterval);  // Stops the slideshow
//   document.body.classList.remove('slideshow-active'); // Removes the fullscreen view
// });

document.body.addEventListener('click', function(event) {
      console.log("Body clicked!");
      clearInterval(slideInterval);  // Stops the slideshow
      document.body.classList.remove('slideshow-active'); // Removes the fullscreen view

      // Redirect to the carousel page.
      list_id = document.getElementById('list_id').getAttribute('data-list-id');
      window.location.href = "/lists/carousel/" + list_id; // Replace with your correct path
      toggleNavbar()
});


// function toggleNavbar() {
//   let navbar = document.querySelector('.navbar');
//   if (navbar) {
//     navbar.classList.toggle('hidden');
//   }
// }

function toggleNavbar() {
  let elementsToToggle = ['.navbar', '#headerText', '#startSlideshow']; // Array of selectors
  elementsToToggle.forEach(selector => {
    let element = document.querySelector(selector);
    if (element) {
      element.classList.toggle('hidden');
    }
  });
}
