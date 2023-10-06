// Hides the category form and shows the "Add a Category?" button.
function cancelCategoryForm() {
  const categoryForm = document.getElementById("categoryForm");
  const addCategory = document.getElementById("addCategory");

  // If the category form element exists, hide it.
  if (categoryForm) {
      categoryForm.style.display = "none"; // hide the category form
  }

  // If the "Add a Category?" button exists, display it as an inline block.
  if (addCategory) {
      addCategory.style.display = "inline-block"; // show the "Add a Category?" button
  }
}

// Fetch the CSRF token from the hidden HTML element for security purposes during POST requests.
const csrfToken = document.getElementById("csrfToken").value;

// Obtain a reference to the "add category" form.
const updateCategoryForm = document.getElementById('addCategoryForm');
// If the form element exists, add an event listener for the form submission event.
if (addCategoryForm) {
    addCategoryForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // Make an asynchronous fetch request to submit form data.
        fetch(this.action, {
            method: 'POST',
            body: new FormData(this),
            headers: {
                'X-CSRFToken': document.getElementById("csrfToken").value,
            },
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response based on the status property of the response data.
            if (data.status === "success") {
                // If the status is "success", redirect to the provided URL (typically list_details.html).
                window.location.href = data.redirect_url; // Redirect to list_details.html
            } else if (data.status === "error") {
                // If the status is "error", show an alert with the provided error message.
                alert(data.message);
            }
        })
        .catch(error => {
            // Log any errors that occur during the fetch process.
            console.error("An error occurred:", error.message);
        });
    });
}


 