
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('save-settings-button').addEventListener('click', submitChangeSettingsForm);
});


function submitChangeSettingsForm() {
    const user_name = document.getElementById('user-name').value;
    const first_name = document.getElementById('first-name').value;
    const last_name = document.getElementById('last-name').value;
    const pfp = document.getElementById('fileInput').files[0];


    var formData = new FormData();
    formData.append('file', pfp);
    formData.append('username', user_name);
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);

    // Get the CSRF token from the cookie
    let csrf_token = document.cookie.split('; ')  
    .find(row => row.startsWith("csrf_access_token" + '=')) 
    ?.split('=')[1];  

    const data = {
        username: user_name,
        first_name: first_name,
        last_name: last_name,
        pfp: pfp
    };
    

    fetch('/user/settings', {
        method: 'POST',
        body: formData,
        headers: {
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
        console.log(data);
        
        const usernameValue = data.username; // The value of the cookie
        if (usernameValue !== ""){
            const daysToExpire = 7; // Duration in days for the cookie to expire
            const date = new Date(); // Current date
            date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000)); // Calculate expiration date
            const expires = "expires=" + date.toUTCString(); // Format expiration as a UTC string
            document.cookie = "username=" + usernameValue + ";" + expires + ";path=/"; // Set the cookie

        }

     
            window.location.href = '/user/settings'; // Redirect to the settings page
       
       
    })

    .catch((error) => {
        const errorMessage = JSON.parse(error.message);
        if (errorMessage.username === 'Username already exists'){
            document.getElementById('username-alr-exists').classList.remove('d-none');
        }
        
        

       
        
    });
    
   
}
