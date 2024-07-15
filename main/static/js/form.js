// main/static/js/form.js

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get references to the form options and sections
    const uploadOption = document.getElementById('uploadImage');
    const captureOption = document.getElementById('captureImage');
    const uploadSection = document.getElementById('uploadSection');
    const captureSection = document.getElementById('captureSection');

    // Add an event listener for changes to the upload option
    uploadOption.addEventListener('change', () => {
        if (uploadOption.checked) {
            // Show the upload section and hide the capture section if upload is selected
            uploadSection.style.display = 'block';
            captureSection.style.display = 'none';
        }
    });

    // Add an event listener for changes to the capture option
    captureOption.addEventListener('change', () => {
        if (captureOption.checked) {
            // Show the capture section and hide the upload section if capture is selected
            uploadSection.style.display = 'none';
            captureSection.style.display = 'block';
        }
    });

    // Initialize the Leaflet map
    const map = L.map('map').setView([0, 0], 13); // Default center and zoom level
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Get geolocation data
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lon;

            // Update the map view
            map.setView([lat, lon], 13);
            L.marker([lat, lon]).addTo(map);

            // Fetch address from latitude and longitude using Nominatim API
            fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
                .then(response => response.json())
                .then(data => {
                    if (data.address) {
                        document.getElementById('address').value = data.display_name; // Populate the address field
                    }
                })
                .catch(error => console.error('Error fetching address:', error));
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
});
