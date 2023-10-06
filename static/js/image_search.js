console.log("Script Loaded"); 

document.addEventListener('DOMContentLoaded', function() {
  console.log("DOMContentLoaded fired");

  // Fetch list_id from the hidden input field
  const list_id = document.getElementById('list_id').value;  
  console.log('from image_search.js, list_id: ', list_id)

  // Search form functionality
  document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;
    window.location.href = `/images/image_response/${list_id}?search_query=${query}`;
  });

});
