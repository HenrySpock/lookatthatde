document.getElementById('addFieldBtn').addEventListener('click', function() {
  let container = document.getElementById('fieldsContainer');
  
  // Create a new field container for each group of elements
  let fieldGroup = document.createElement('div');
  fieldGroup.className = "field-container row mt-2";

  // Create input for field name
  let nameCol = document.createElement('div');
  nameCol.className = "col-md-5";
  let input = document.createElement('input');
  input.setAttribute('type', 'text');
  input.setAttribute('name', 'field_names[]');
  input.className = "form-control limited-width";  // add the Bootstrap class
  nameCol.appendChild(input);
  fieldGroup.appendChild(nameCol);

  // Create radio buttons for type
  let typeCol = document.createElement('div');
  typeCol.className = "col-md-2";
  let radioText = document.createElement('input');
  radioText.setAttribute('type', 'radio');
  radioText.setAttribute('name', 'field_types[]');
  radioText.setAttribute('value', 'text');
  radioText.setAttribute('checked', 'checked');
  typeCol.appendChild(radioText);
  let textLabel = document.createElement('label');
  textLabel.innerHTML = " Text";
  textLabel.className = "radio-spacing"; // apply the styling
  textLabel.insertBefore(radioText, textLabel.firstChild);
  typeCol.appendChild(textLabel);

  let radioNumber = document.createElement('input');
  radioNumber.setAttribute('type', 'radio');
  radioNumber.setAttribute('name', 'field_types[]');
  radioNumber.setAttribute('value', 'number');
  typeCol.appendChild(radioNumber);
  let numberLabel = document.createElement('label');
  numberLabel.innerHTML = " Number";
  numberLabel.insertBefore(radioNumber, numberLabel.firstChild);
  typeCol.appendChild(numberLabel);

  fieldGroup.appendChild(typeCol);

  // Create the delete button
  let deleteCol = document.createElement('div');
  deleteCol.className = "col-md-5";
  let deleteBtn = document.createElement('button');
  deleteBtn.innerText = "Delete this Field?";
  deleteBtn.type = "button";
  deleteBtn.className = "btn btn-danger btn-block limited-width";  // add the Bootstrap class
  deleteBtn.onclick = function() {
      fieldGroup.remove();
  };
  deleteCol.appendChild(deleteBtn);
  fieldGroup.appendChild(deleteCol);

  // Add the entire group to the container
  container.appendChild(fieldGroup);

  // Add a break for clarity
  fieldGroup.appendChild(document.createElement('br'));
});


function deleteField(fieldId) {
  // var fieldContainer = document.querySelector('.field-container[data-id="' + fieldId + '"]');
  let fieldContainer = document.querySelector('.field-container[data-field-id="' + fieldId + '"]');
  if (fieldContainer) {
      // Instead of removing, hide it and mark it for deletion
      fieldContainer.style.display = 'none';

      // Create a hidden input inside the fieldContainer to mark it for deletion
      let hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'delete_field_ids[]';  // Use array notation
      hiddenInput.value = fieldId;
      fieldContainer.appendChild(hiddenInput);
  }
}

 