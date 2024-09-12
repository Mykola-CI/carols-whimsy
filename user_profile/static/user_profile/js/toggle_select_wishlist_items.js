// Get master checkbox
const masterCheckbox = document.getElementById('wishlist-master');
// Select all product checkboxes
const checkboxes = document.querySelectorAll('.select-card-check');
// Get the label for the master checkbox
const masterLabel = document.querySelector('label[for="wishlist-master"]');

// Add event listener to the master checkbox
masterCheckbox.addEventListener('change', function () {
    const isChecked = masterCheckbox.checked;
    // Select or deselect all checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
    });
    // Change label text based on selection state
    masterLabel.textContent = isChecked ? 'Unselect all' : 'Select all';
});