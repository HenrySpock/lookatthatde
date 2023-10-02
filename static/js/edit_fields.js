

// document.getElementById('addFieldBtn').addEventListener('click', function() {
//   var container = document.getElementById('fieldsContainer');

//   // Create input for field name
//   var input = document.createElement('input');
//   input.setAttribute('type', 'text');
//   input.setAttribute('name', 'field_names[]'); // Use array notation to capture multiple inputs
//   container.appendChild(input);

//   // Create radio buttons for type
//   var radioText = document.createElement('input');
//   radioText.setAttribute('type', 'radio');
//   radioText.setAttribute('name', 'field_types[]');
//   radioText.setAttribute('value', 'text');
//   container.appendChild(radioText);
//   container.innerHTML += "Text";

//   var radioNumber = document.createElement('input');
//   radioNumber.setAttribute('type', 'radio');
//   radioNumber.setAttribute('name', 'field_types[]');
//   radioNumber.setAttribute('value', 'number');
//   container.appendChild(radioNumber);
//   container.innerHTML += "Number";

//   // Add a break for clarity
//   container.appendChild(document.createElement('br'));
// });

// function deleteField(fieldId) {
//   // JavaScript logic to mark the field for deletion or remove the DOM element
//   // Depending on how you implement deletion, this can vary.
//   // Simplest approach: remove the DOM element. But you need backend logic to handle actual deletions.
//   var fieldContainer = document.querySelector('.field-container[data-id="' + fieldId + '"]');
//   if (fieldContainer) {
//       fieldContainer.remove();
//   }
// }

document.getElementById('addFieldBtn').addEventListener('click', function() {
  var container = document.getElementById('fieldsContainer');
  
  // Create a new field container for each group of elements
  var fieldGroup = document.createElement('div');
  fieldGroup.className = "field-container";
  
  // Create input for field name
  var input = document.createElement('input');
  input.setAttribute('type', 'text');
  input.setAttribute('name', 'field_names[]'); // Use array notation to capture multiple inputs
  fieldGroup.appendChild(input);

  // Create radio buttons for type
  var radioText = document.createElement('input');
  radioText.setAttribute('type', 'radio');
  radioText.setAttribute('name', 'field_types[]');
  radioText.setAttribute('value', 'text');
  fieldGroup.appendChild(radioText);
  var textLabel = document.createElement('span');
  textLabel.innerHTML = "Text";
  fieldGroup.appendChild(textLabel);

  var radioNumber = document.createElement('input');
  radioNumber.setAttribute('type', 'radio');
  radioNumber.setAttribute('name', 'field_types[]');
  radioNumber.setAttribute('value', 'number');
  fieldGroup.appendChild(radioNumber);
  var numberLabel = document.createElement('span');
  numberLabel.innerHTML = "Number";
  fieldGroup.appendChild(numberLabel);

  // Create the delete button
  var deleteBtn = document.createElement('button');
  deleteBtn.innerText = "Delete this Field?";
  deleteBtn.type = "button";
  deleteBtn.onclick = function() {
      fieldGroup.remove();
  };
  fieldGroup.appendChild(deleteBtn);

  // Add the entire group to the container
  container.appendChild(fieldGroup);

  // Add a break for clarity
  fieldGroup.appendChild(document.createElement('br'));
});


function deleteField(fieldId) {
  // var fieldContainer = document.querySelector('.field-container[data-id="' + fieldId + '"]');
  var fieldContainer = document.querySelector('.field-container[data-field-id="' + fieldId + '"]');
  if (fieldContainer) {
      // Instead of removing, hide it and mark it for deletion
      fieldContainer.style.display = 'none';

      // Create a hidden input inside the fieldContainer to mark it for deletion
      var hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'delete_field_ids[]';  // Use array notation
      hiddenInput.value = fieldId;
      fieldContainer.appendChild(hiddenInput);
  }
}


// function submitFieldsForm() {
//   let form = document.getElementById('dynamicFieldsForm');
//   let formData = new FormData(document.getElementById('dynamicFieldsForm'));

// // Now, make the fetch POST request
// fetch('/edit_fields/' + listId, {
//   method: 'POST',
//   headers: {
//       'X-CSRFToken': csrfToken
//   },
//   body: formData
// })
// .then(response => response.json())
// .then(data => {
//   if (data.success) {
//       // Show the success message as a flash message
//       // Assuming you have some flash message mechanism in place (like a function named `showFlashMessage`)
//       showFlashMessage(data.message, "success"); // if there's no such function, you can replace this with alert(data.message) or any other mechanism to show the message

//       // Redirect to list_details
//       window.location.href = `/list_details/${listId}`; // adjust the path if it's different
//   } else {
//       // Handle error
//       alert(data.message || "An error occurred.");
//   }
// })
// .catch(error => {
//   // Handle fetch errors
//   console.error("Fetch error: ", error);
//   alert("An unexpected error occurred.");
// });
// }

// // Attach the submitFieldsForm function to the form's submit event
// document.getElementById('dynamicFieldsForm').addEventListener('submit', function(event) {
//   event.preventDefault();
//   submitFieldsForm();
// });
