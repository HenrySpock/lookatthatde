function cancelCategoryForm() {
  const categoryForm = document.getElementById("categoryForm");
  const addCategory = document.getElementById("addCategory");

  if (categoryForm) {
      categoryForm.style.display = "none"; // hide the category form
  }

  if (addCategory) {
      addCategory.style.display = "inline-block"; // show the "Add a Category?" button
  }
}

const csrfToken = document.getElementById("csrfToken").value;

const updateCategoryForm = document.getElementById('addCategoryForm');
if (addCategoryForm) {
    addCategoryForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        fetch(this.action, {
            method: 'POST',
            body: new FormData(this),
            headers: {
                'X-CSRFToken': document.getElementById("csrfToken").value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect_url; // Redirect to list_details.html
            } else if (data.status === "error") {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("An error occurred:", error.message);
        });
    });
}


 