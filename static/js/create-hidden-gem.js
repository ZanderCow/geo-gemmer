
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-gem-submit-button').addEventListener('click', createHiddenGem);
});


function createHiddenGem() {
    const gemName = document.getElementById('gem-name').value;
    const gemType = document.getElementById('gem-type').value;
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const wheelchairAccessible = document.getElementById('wheelchair_accessible').checked;
    const serviceAnimalFriendly = document.getElementById('service_animal_friendly').checked;
    const multilingualSupport = document.getElementById('multilingual_support').checked;
    const brailleSignage = document.getElementById('braille_signage').checked;
    const largePrintMaterials = document.getElementById('large_print_materials').checked;
    const accessibleRestrooms = document.getElementById('accessible_restrooms').checked;
    const hearingAssistance = document.getElementById('hearing_assistance').checked;
    const img1 = document.getElementById('image-input').files[0];
    const img2 = document.getElementById('image-input').files[1];
    const img3 = document.getElementById('image-input').files[3];

    console.log(img1, img2, img3);

    var formData = new FormData();
    formData.append('gem_name', gemName);
    formData.append('gem_type', gemType);
    formData.append('latitude', latitude);
    formData.append('longitude', longitude);
    formData.append('wheelchair_accessible', wheelchairAccessible);
    formData.append('service_animal_friendly', serviceAnimalFriendly);
    formData.append('multilingual_support', multilingualSupport);
    formData.append('braille_signage', brailleSignage);
    formData.append('large_print_materials', largePrintMaterials);
    formData.append('accessible_restrooms', accessibleRestrooms);
    formData.append('hearing_assistance', hearingAssistance);
    formData.append('image_1', img1);
    formData.append('image_2', img2);
    formData.append('image_3', img3);

    
    /*
    // Get the CSRF token from the cookie
    let csrf_token = document.cookie.split('; ')  
    .find(row => row.startsWith("csrf_access_token" + '=')) 
    ?.split('=')[1];  

    

    fetch('/user/create-gem', {
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
     
            window.location.href = '/user/settings'; // Redirect to the settings page
       
       
    })

    .catch((error) => {
        const errorMessage = JSON.parse(error.message);
        if (errorMessage.username === 'Username already exists'){
            document.getElementById('username-alr-exists').classList.remove('d-none');
        }
        
        

       
        
    });
    */
   
}
