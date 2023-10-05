function openReportModal(listId, creatorId) {
  console.log("List ID passed to openReportModal:", listId);
  console.log("Type of listId:", typeof listId);
  console.log('Reported list id: ', listId, ', and reported creator id: ', creatorId)

  // Log the element before setting its value
  let elem = document.getElementById('reportListId');
  console.log("Element with ID 'reportListId':", elem);

  // Set the list ID and creator ID in hidden input fields
  document.getElementById('reportListId').value = listId;
  document.getElementById('reportCreatorId').value = creatorId;

  // Display the modal
  let modal = document.getElementById('reportModal');
  modal.style.display = "block";
}

// Close the modal function
function closeReportModal() {
  let modal = document.getElementById('reportModal');
  modal.style.display = "none";
}

// Close the modal when pressing the Escape key
document.addEventListener('keydown', function(event) {
  if (event.key === "Escape") {
    closeReportModal();
  }
});

// Close the modal when clicking outside
let modal = document.getElementById('reportModal');
window.onclick = function(event) {
  if (event.target == modal) {
    closeReportModal();
  }
}