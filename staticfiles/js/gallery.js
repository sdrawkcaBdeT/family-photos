let currentPhotoId = null;

function openModal(url, id) {
    const modal = document.getElementById('photoModal');
    const modalImage = document.getElementById('modalImage');
    const modalComments = document.getElementById('modalComments');
    const sourceComments = document.getElementById(`comments-${id}`);

    currentPhotoId = id;
    modalImage.src = url;

    // Copy comments
    modalComments.innerHTML = sourceComments.innerHTML;

    modal.showModal();

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
}

function closeModal() {
    document.getElementById('photoModal').close();
    currentPhotoId = null;
}

document.getElementById('sendCommentBtn').addEventListener('click', () => {
    const input = document.getElementById('commentInput');
    const text = input.value.trim();

    if (!text || !currentPhotoId) return;

    const csrfToken = getCookie('csrftoken');

    fetch(`/photo/${currentPhotoId}/comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ text: text })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                // Append to modal
                const div = document.createElement('div');
                div.className = 'comment';
                div.innerHTML = `<strong>${data.author}:</strong> ${data.text}`;
                document.getElementById('modalComments').appendChild(div);

                // Append to hidden list (so it persists if reopened)
                const sourceComments = document.getElementById(`comments-${currentPhotoId}`);
                const hiddenDiv = div.cloneNode(true);
                sourceComments.appendChild(hiddenDiv);

                input.value = '';
            }
        });
});

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
