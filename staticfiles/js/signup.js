// main/static/js/signup.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signupForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
        });
        
        const result = await response.json();
        const messageDiv = document.getElementById('form-message');

        if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.style.color = 'green';
            // redirect to login page after successful signup
            window.location.href = '/login/';
        } else {
            messageDiv.textContent = result.error;
            messageDiv.style.color = 'red';
        }
    });
});
