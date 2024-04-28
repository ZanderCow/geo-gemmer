document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('save-changes-button').addEventListener('click', changeReview);
});


function changeReview() {
    const rating = document.getElementById('rating').value;
    const review = document.getElementById('review').value;
    const review_id = document.getElementById("review-id").textContent
    
    

    const data = {
        rating: rating,
        review: review,
        review_id: review_id
    };
    
    // Get the CSRF token from the cookie
    let csrf_token = document.cookie.split('; ')  
    .find(row => row.startsWith("csrf_access_token" + '=')) 
    ?.split('=')[1]; 

    fetch(`/review/${review_id}/edit-review`, {
        method: 'POST',
        body: JSON.stringify(data), // Converting the JSON object to a JSON string
        headers: {
             'Content-Type': 'application/json',
             'X-CSRF-Token': csrf_token // The CSRF token you retrieved from your cookie or elsewhere
             }, // Setting the Content-Type as application/json
        credentials: 'include'  // Necessary to include cookies with requests
    })

    .then((response) => {
        if (response.ok) {
            return response.json();
        } 
        else {
            return response.text().then(text => {
                throw new Error(text);
            });
        }
    })

    .then(data => { 
        
            window.location.href = '/user'; // Redirect to the settings page
       
       
    })

    .catch((error) => {
        const errorMessage = JSON.parse(error.message);
        if (errorMessage.rating === 'rating out of range'){
            document.getElementById('rating-out-of-bounds').classList.remove('d-none');
        }
        
        

       
        
    });
    
   
}
