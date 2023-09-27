// // For Adding New Fields
// document.getElementById("addFieldButton").addEventListener("click", function() {
//   const fieldContainer = document.getElementById("fieldsContainer");
//   const fieldName = document.getElementById("newFieldName").value;
//   const fieldType = document.querySelector('input[name="fieldType"]:checked').value;

//   if (!fieldName.trim()) {
//       alert("Field name cannot be empty!");
//       return;
//   }

//   const fieldWrapper = document.createElement("div");
//   fieldWrapper.className = "fieldWrapper";

//   const fieldLabel = document.createElement("label");
//   fieldLabel.textContent = fieldName;

//   const fieldInput = document.createElement("input");
//   fieldInput.name = fieldName;
//   fieldInput.type = fieldType === "text" ? "text" : "number";

//   const deleteButton = document.createElement("button");
//   deleteButton.textContent = "Delete";
//   deleteButton.addEventListener("click", function() {
//       fieldWrapper.remove();
//   });

//   fieldWrapper.appendChild(fieldLabel);
//   fieldWrapper.appendChild(fieldInput);
//   fieldWrapper.appendChild(deleteButton);

//   fieldContainer.appendChild(fieldWrapper);
// });
 