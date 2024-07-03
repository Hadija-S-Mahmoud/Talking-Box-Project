// main/static/js/form.js
document.addEventListener('DOMContentLoaded', () => {
    const uploadOption = document.getElementById('uploadImage');
    const captureOption = document.getElementById('captureImage');
    const uploadSection = document.getElementById('uploadSection');
    const captureSection = document.getElementById('captureSection');

    uploadOption.addEventListener('change', () => {
        if (uploadOption.checked) {
            uploadSection.style.display = 'block';
            captureSection.style.display = 'none';
        }
    });

    captureOption.addEventListener('change', () => {
        if (captureOption.checked) {
            uploadSection.style.display = 'none';
            captureSection.style.display = 'block';
        }
    });
});
