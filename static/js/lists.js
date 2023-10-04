// Grabs all the category cards and attaches an event listener to them
document.addEventListener("DOMContentLoaded", function() {
    const radioButtons = document.querySelectorAll('input[type="radio"][name="listType"]');
    radioButtons.forEach(button => {
        button.addEventListener("change", function() {
            displayGroups();
            resetAllLists();  // Reset all lists to be hidden
        });
    });

    // Reset all lists to be hidden
    function resetAllLists() {
        const allListDivs = document.querySelectorAll('[data-lists-for]');
        allListDivs.forEach(div => {
            div.style.display = 'none';
        });
    }

    // Display default grouping
    displayGroups();

// Handle category card clicks
const categoryCards = document.querySelectorAll('.category-card');
categoryCards.forEach(card => {
    card.addEventListener('click', function() {
        console.log('Category card clicked!');  // Debugging line
        const currentGroup = card.closest('[data-group]');
        
        console.log('Looking for lists with data-category-id:', card.getAttribute('data-category-id'));

        const associatedListDiv = currentGroup.querySelector(`[data-lists-for="${card.getAttribute('data-category-id')}"]`);
        
        if (associatedListDiv) {
            console.log('Associated lists found!');
            
            // If the category was already expanded, collapse it.
            if (associatedListDiv.getAttribute('data-expanded') === "true") {
                associatedListDiv.style.display = 'none';
                associatedListDiv.setAttribute('data-expanded', 'false');
            } else {
                // Collapse all the categories first
                const allListDivsInGroup = currentGroup.querySelectorAll('[data-lists-for]');
                allListDivsInGroup.forEach(div => {
                    div.style.display = 'none';
                    div.setAttribute('data-expanded', 'false');
                });
                
                // Then expand the selected category
                associatedListDiv.style.display = "block";
                associatedListDiv.setAttribute('data-expanded', 'true');
            }

        } else {
            console.log('No associated lists found.');
        }
    });        
});

});

// Display the selected group
function displayGroups() {
    const selectedValue = document.querySelector('input[type="radio"][name="listType"]:checked').value;
    const groups = document.querySelectorAll('[data-group]');
    
    groups.forEach(group => {
        if (group.getAttribute('data-group') === selectedValue) {
            group.style.display = 'block';
        } else {
            group.style.display = 'none';
        }
    });
}

