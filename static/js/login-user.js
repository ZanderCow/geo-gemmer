
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-submit-button').addEventListener('click', submitLoginForm);
});


function submitLoginForm() {
    const user_name = document.getElementById('username').value;
    const password = document.getElementById('password').value;
   

    // make errors messages disappear when the user clicks the submit button
    document.getElementById('usernme-or-pssword-error').classList.add('d-none');
    // prepare data to send, using FormData or a JSON object
    const data = {
        username: user_name,
        password: password,
    };

    // Sending the data as JSON
    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(data), // Converting the JSON object to a JSON string
        headers: { 'Content-Type': 'application/json' }, // Setting the Content-Type as application/json
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
        document.body.innerHTML = `
        <section class="py-4 py-xl-5">
            <div class="container h-100">
                <div class="row h-100">
                    <div class="col-md-10 col-xl-8 text-center d-flex d-sm-flex d-md-flex justify-content-center align-items-center mx-auto justify-content-md-center align-items-md-center justify-content-lg-center justify-content-xl-center" style="padding-top: 200px;">
                        <div><img src="../static/img/geo-gemmer-logo.png" width="157" height="72">
                            <h1 class="display-6 fs-1 fw-bold mb-3" style="padding-top: 30px;">Logging You in</h1>
                            <p class="mb-4">Shouldn't be too long. Hang tight!</p><span class="spinner-grow" role="status" style="color: var(--bs-primary);"></span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        `;
        
        setTimeout(() => {
            window.location.href = '/user';
        }, 3000);
       
    })

    .catch((error) => {
        const errorMessage = JSON.parse(error.message);
        console.log(errorMessage);
        if (errorMessage.error === "username or password is incorrect"){
            document.getElementById('usernme-or-pssword-error').classList.remove('d-none');
        }
        
        

       
        
    });
    
   
}
