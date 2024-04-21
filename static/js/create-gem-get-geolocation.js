document.addEventListener("DOMContentLoaded", function() {
    const getCoordinatesButton = document.getElementById('get-location-button');
    
    getCoordinatesButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevents the form from submitting

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;

            }, function(error) {
                console.error('Error Code = ' + error.code + ' - ' + error.message);
                alert('Error obtaining location: ' + error.message);
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });
});