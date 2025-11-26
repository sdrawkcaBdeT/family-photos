document.addEventListener('DOMContentLoaded', () => {
    const fileElem = document.getElementById('fileElem');
    const uploadBtn = document.getElementById('uploadBtn');
    const progressOverlay = document.getElementById('progressOverlay');
    const uploadCountSpan = document.getElementById('uploadCount');

    uploadBtn.addEventListener('click', () => {
        fileElem.click();
    });

    fileElem.addEventListener('change', handleFiles);

    function handleFiles() {
        const files = this.files;
        if (!files.length) return;

        uploadCountSpan.textContent = files.length;
        progressOverlay.classList.remove('hidden');

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        // Add CSRF token
        const csrfToken = getCookie('csrftoken');

        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    location.reload(); // Simple refresh to show new photos
                } else {
                    alert('Upload failed');
                    progressOverlay.classList.add('hidden');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Upload error');
                progressOverlay.classList.add('hidden');
            });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
