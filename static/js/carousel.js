// Variables to control the slideshow
let slideIndex = 0;
let slideInterval;
let slides = document.getElementsByClassName("mySlides");

// Function to cycle through the slides
function showSlides() {
    console.log("showSlides triggered");
    
    // Hide all slides
    for (let i = 0; i < slides.length; i++) {
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
    let elementsToToggle = ['.navbar', '#headerText', '#startSlideshow', '#list-details', '#slideshowSpeed', '#slideshowSpeedLabel'];
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
        // slideInterval = setInterval(showSlides, 1500); // Start the slideshow
        let speed = document.getElementById('slideshowSpeed').value || 1500;
        slideInterval = setInterval(showSlides, speed);
    });

    // Add event listener for stopping the slideshow and redirecting back to the carousel
    let slideshowContainer = document.querySelector('.slideshow-container');
    slideshowContainer.addEventListener('click', function(event) { 

        // document.body.addEventListener('click', function(event) {

        console.log("Slideshow container clicked!");

        clearInterval(slideInterval);  // Stop the slideshow

        // Redirect to the carousel page
        let list_id = document.getElementById('list_id').getAttribute('data-list-id');
        window.location.href = "/lists/carousel/" + list_id;
        
        toggleDisplay(); // Toggle visibility of navigation and controls
});
}

document.body.addEventListener('keydown', function(event) {
    if (event.key === "ArrowLeft") {
        slideIndex -= 2; 
        if (slideIndex < 0) {  // Add this check
            slideIndex = slides.length - 1;  // Set to last slide
        }
        clearInterval(slideInterval);
        showSlides();
    } else if (event.key === "ArrowRight") {
        if (slideIndex >= slides.length) {  // Add this check
            slideIndex = 0;  // Set to first slide
        }
        clearInterval(slideInterval);
        showSlides();
    } else if (event.key === "Enter") {
        let speed = document.getElementById('slideshowSpeed').value || 1500;
        slideInterval = setInterval(showSlides, speed);
    }
});

document.getElementById('slideshowSpeed').addEventListener('change', function() {
    console.log("Raw value:", this.value);
    clearInterval(slideInterval);  // Clear the current slideshow interval
    slideInterval = 0;
    console.log('slideInterval: ', slideInterval)

    // Get the new speed from the dropdown (converted to milliseconds)
    let speed = parseInt(this.value, 10);
    console.log("New speed:", speed);
    slideInterval = setInterval(showSlides, speed);  // Start the slideshow with the new speed
});