// main/static/js/issues.js

function toggleDropdown(issueId) {
    const dropdown = document.getElementById(`dropdown-${issueId}`);
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
}

// Wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Create a WebSocket connection to the issues endpoint
    const issueSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/issues/'
    );

    // Handle incoming messages from the WebSocket
    issueSocket.onmessage = function(e) {
        const data = JSON.parse(e.data); // Parse the JSON data received from the server
        const issueId = data.issue_id; // Get the issue ID from the data
        const newStatus = data.status; // Get the new status from the data
        const newProgressReport = data.progress_report; // Get the new progress report from data

        // Find the element for the issue and update its status on the page
        const issueElement = document.querySelector(`#issue-${issueId}`);
        if (issueElement) {
            issueElement.querySelector('.issue-status').textContent = `Status: ${newStatus}`;
            issueElement.querySelector('.issue-progress-report').textContent = `Progress Report: ${newProgressReport}`;
        }
    };

    // Handle WebSocket connection closure
    issueSocket.onclose = function(e) {
        console.error('Issue WebSocket closed unexpectedly');
    };

    // Add a submit event listener to all forms with the class 'issue-status-form'
    document.querySelectorAll('.issue-status-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the default form submission

            const issueId = form.dataset.issueId; // Get the issue ID from the form's data attribute
            const newStatus = form.querySelector('select').value; // Get the new status from the form's select element

            // Send the new status to the WebSocket server
            issueSocket.send(JSON.stringify({
                'issue_id': issueId,
                'status': newStatus
            }));
        });
    });
});
