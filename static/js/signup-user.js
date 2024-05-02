
document.addEventListener('DOMContentLoaded', function() {
document.getElementById('sign-up-submit-button').addEventListener('click', submitSignupForm);
});


function submitSignupForm() {
const user_name = document.getElementById('username').value;
const password = document.getElementById('password').value;

// Prepare data to send, using FormData or a JSON object

const data = {
    username: user_name,
    password: password,
};

// Sending the data as JSON
fetch('/sign-up', {
    method: 'POST',
    body: JSON.stringify(data), // Converting the JSON object to a JSON string
    headers: { 'Content-Type': 'application/json' }, // Setting the Content-Type as application/json
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
    // Redirect to the login page
    window.location.href = '/user/setup';
})

.catch((error) => {
    const errorMessage = JSON.parse(error.message);
    console.log(errorMessage);
    if (errorMessage.username === "Username is required"){
        document.getElementById('please-enter-username-message').classList.remove('d-none');
    }
    if (errorMessage.username === "Username already exists"){
        document.getElementById('user-alr-exists-message').classList.remove('d-none');
    }
    if (errorMessage.password === "Password is required"){
        document.getElementById('please-enter-password-message').classList.remove('d-none');
    }
    

    
    
});


}
