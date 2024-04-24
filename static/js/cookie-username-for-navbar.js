function getUsernameCookie() {
    const cookies = document.cookie; // Get all cookies as a single string
    const cookiesArray = cookies.split('; '); // Split the cookies string into an array of "key=value" strings

    // Loop through the array to find the "username" cookie
    for (let i = 0; i < cookiesArray.length; i++) {
        const cookiePair = cookiesArray[i].split('='); // Split each "key=value" string into [key, value]
        if (cookiePair[0] === 'username') {
            return cookiePair[1]; // Return the value of the "username" cookie
        }
    }
}

function setUsername() {
    var username = getCookie('username');  // Retrieve the username from cookies
    var usernameElement = document.getElementById('username');
    if (username && usernameElement) {
        usernameElement.innerText = username;  // Set the text of the element
    }
    console.log(username);
}

window.onload = function() {
    setUsername();  // Call setUsername when the page has fully loaded
};

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
