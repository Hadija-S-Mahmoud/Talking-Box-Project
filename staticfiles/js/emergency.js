// main/static/js/emergencycontacts.js
// JavaScript for Emergency Contacts page
// Future enhancements and functionality can be added here

// Example: Adding click event listeners to contact links
document.addEventListener('DOMContentLoaded', function() {
    const contactLinks = document.querySelectorAll('.contact-link');
    
    contactLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const phoneNumber = event.target.getAttribute('href');
            console.log(`Calling: ${phoneNumber}`);
            // Additional functionality can be added here if needed
        });
    });
});
