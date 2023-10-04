// Variables to control the slideshow
var slideIndex = 0;
var slideInterval;
var slides = document.getElementsByClassName("mySlides");

// Function to cycle through the slides
function showSlides() {
    console.log("showSlides triggered");
    
    // Hide all slides
    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Display the next slide
    if (slideIndex >= slides.length) {
        slideIndex = 0; // Reset to the first slide if we've reached the end
    }
    slides[slideIndex].style.display = "block";
    slideIndex++;
}

// Function to toggle display of specific elements
function toggleDisplay() {
    let elementsToToggle = ['.navbar', '#headerText', '#startSlideshow', '#list-details'];
    elementsToToggle.forEach(selector => {
        let element = document.querySelector(selector);
        if (element) {
            element.classList.toggle('hidden');
        }
    });
}

// Check if the current page is the slideshow page
if (window.location.pathname.includes("/slideshow/")) {
    // Once the page is fully loaded
    document.addEventListener("DOMContentLoaded", function() {
        toggleDisplay(); // Toggle visibility of navigation and controls
        showSlides();    // Display the first slide
        slideInterval = setInterval(showSlides, 2000); // Start the slideshow
    });
}

// Add event listener for stopping the slideshow and redirecting back to the carousel
document.body.addEventListener('click', function(event) {
    console.log("Body clicked!");

    clearInterval(slideInterval);  // Stop the slideshow

    // Redirect to the carousel page
    let list_id = document.getElementById('list_id').getAttribute('data-list-id');
    window.location.href = "/lists/carousel/" + list_id;
    
    toggleDisplay(); // Toggle visibility of navigation and controls
});



 