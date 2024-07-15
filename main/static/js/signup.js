// main/static/js/signup.js

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get the signup form element
    const form = document.getElementById('signupForm');

    // Add a submit event listener to the signup form
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
        
        // Create a FormData object from the form
        const formData = new FormData(form);

        // Send the form data to the server using Fetch API
        const response = await fetch(form.action, {
            method: 'POST', // Use POST method for form submission
            body: formData, // Send form data as the request body
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Indicate that this is an AJAX request
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Include CSRF token for security
            },
        });

        // Parse the JSON response from the server
        const result = await response.json();
        const messageDiv = document.getElementById('form-message'); // Get the message div element

        if (response.ok) {
            // Display success message and redirect to the login page
            messageDiv.textContent = result.message;
            messageDiv.style.color = 'green';
            setTimeout(() => {
                window.location.href = '/login/'; // Redirect to the login page after successful signup
            }, 2000); // Delay to let the user see the success message
        } else {
            // Display error message
            messageDiv.textContent = result.error;
            messageDiv.style.color = 'red';
        }
    });
});
