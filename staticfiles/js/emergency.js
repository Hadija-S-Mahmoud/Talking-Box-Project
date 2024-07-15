// main/static/js/emergencycontacts.js

// JavaScript for Emergency Contacts page
// Future enhancements and functionality can be added here

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with the class 'contact-link'
    const contactLinks = document.querySelectorAll('.contact-link');
    
    // Loop through each contact link
    contactLinks.forEach(link => {
        // Add a click event listener to each link
        link.addEventListener('click', function(event) {
            // Get the phone number from the 'href' attribute of the link
            const phoneNumber = event.target.getAttribute('href');
            // Log the phone number to the console (example of what could be done)
            console.log(`Calling: ${phoneNumber}`);
            // Additional functionality for the click event can be added here
        });
    });
});
