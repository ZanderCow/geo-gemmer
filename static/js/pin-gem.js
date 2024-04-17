document.getElementById('pinGemButton').addEventListener('click', function() {
    const gemId = "{{ gem_basic_info.id }}"; // Ensure these variables are appropriately populated
    const userId = "{{ user.id }}"; // Ensure these variables are appropriately populated

    fetch('/gem/pin-gem/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            gem_id: gemId,
            user_id: userId
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // or .text() if the response is plain text
        } else {
            throw new Error('Something went wrong on the server side.');
        }
    })
    .then(data => {
        const buttonContainer = document.getElementById('pinGemButton').parentElement;
        buttonContainer.innerHTML = '<p class="fw-bold text-success mb-2">Gem Pinned</p>';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});