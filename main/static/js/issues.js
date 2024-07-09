// main/static/js/issues.js

document.addEventListener("DOMContentLoaded", function() {
    const issueSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/issues/'
    );

    issueSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const issueId = data.issue_id;
        const newStatus = data.status;

        // Update the issue status on the page
        const issueElement = document.querySelector(`#issue-${issueId}`);
        if (issueElement) {
            issueElement.querySelector('.issue-status').textContent = `Status: ${newStatus}`;
        }
    };

    issueSocket.onclose = function(e) {
        console.error('Issue WebSocket closed unexpectedly');
    };

    document.querySelectorAll('.issue-status-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const issueId = form.dataset.issueId;
            const newStatus = form.querySelector('select').value;

            issueSocket.send(JSON.stringify({
                'issue_id': issueId,
                'status': newStatus
            }));
        });
    });
});
