document.getElementById('pinGemButton').addEventListener('click', function() {
    const gem_id = gemId// Ensure these variables are appropriately populated
    console.log('gemId:', gem_id);

    const data = {
        gem_id: gem_id,
        // user_id will be passed from auth
    };
    // Get the CSRF token from the cookie
    let csrf_token = document.cookie.split('; ')  
    .find(row => row.startsWith("csrf_access_token" + '=')) 
    ?.split('=')[1];     

    fetch(`/gem/${gem_id}/pin`, {
        method: 'POST',
        body: JSON.stringify(data), // Converting the JSON object to a JSON string
        headers: {
             'Content-Type': 'application/json',
             'X-CSRF-Token': csrf_token // The CSRF token you retrieved from your cookie or elsewhere
             }, // Setting the Content-Type as application/json
        credentials: 'include'  // Necessary to include cookies with requests
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



