document.addEventListener('DOMContentLoaded', function () {
    const formBasic = document.querySelector('#basic_info_form');
    const formPhone = document.querySelector('#user_phone_form');

    // User Basic Info Form submission
    formBasic.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
        const formData = new FormData(formBasic);

        fetch(formBasic.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': formBasic.querySelector('[name=csrfmiddlewaretoken]').value }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the DOM with the new data
                    const titleNameElement = document.querySelector('#title_name');
                    const dateOfBirthElement = document.querySelector('#date_of_birth');

                    // Check if the title is "Prefer not to use" and set it to an empty string if so
                    const title = data.updated_basic.title === 'Prefer not to use' ? '' : data.updated_basic.title;

                    // Construct the new title name
                    const newTitleName = `${title} ${data.updated_basic.first_name} ${data.updated_basic.last_name}`;
                    titleNameElement.textContent = newTitleName;

                    // Update the date of birth:

                    const dateOfBirthString = data.updated_basic.date_of_birth;
                    // Parse the date string into a Date object
                    const dateOfBirth = new Date(dateOfBirthString);
                    // Format the date using Intl.DateTimeFormat
                    const options = { year: 'numeric', month: 'short', day: 'numeric' };
                    let formattedDate = new Intl.DateTimeFormat('en-US', options).format(dateOfBirth);
                    // Insert dot (`.`) after the short for a month
                    formattedDate = formattedDate.replace(/(\w{3}) /, '$1. ');

                    dateOfBirthElement.textContent = formattedDate;

                } else {
                    console.log('Form submission failed:', data.errors || data.message);
                }
                showToast(data);
            })
            .catch(error => console.log('Error:', error));
    });

    // Contact form submission
    formPhone.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
        const formData = new FormData(formPhone);

        fetch(formPhone.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': formPhone.querySelector('[name=csrfmiddlewaretoken]').value }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const phoneElement = document.querySelector('#phone_profile');

                    // Update phone number on the page
                    phoneElement.textContent = data.updated_phone;

                } else {
                    console.log('Form submission failed:', data.errors || data.message);
                }
                showToast(data);
            })
            .catch(error => console.log('Error:', error));
    });

    // AJAX form submission for email
    $('#user_email_form').on('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(), // Serialize the form data
            success: function (response) {
                // Handle success - display a message or update the page
                showToast(response);
            },
            error: function (xhr, status, error) {
                // Log the detailed error for debugging (optional)
                console.error('Error details:', xhr, status, error);

                // Show a generic error message to the user
                showToast({
                    success: false,
                    message: 'An unexpected error occurred. Please try again later.'
                });
            }
        });
    });
    // Show toast message returned with json response
    function showToast(data) {
        // Display Bootstrap toast
        const toastContainer = document.querySelector('#toast-container-json');
        const toastHTML = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true" data-bs-delay="5000">
                <div class="toast-header bg-light">
                    <strong class="me-auto">${data.success ? "Carol's Success Message" : "Carrol's sorry message"}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body fs-base">
                    ${data.message}
                </div>
            </div>
        `;
        toastContainer.innerHTML = toastHTML;
        const toastElement = toastContainer.querySelector('.toast');
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
});
