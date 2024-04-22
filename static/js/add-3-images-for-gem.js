document.getElementById('add-images-button').addEventListener('click', function() {
    document.getElementById('image-input').click();  // Trigger the file input
});

document.getElementById('image-input').addEventListener('change', function() {
    const files = this.files;  // Get all files selected by the user

    // Loop through the selected files, updating the corresponding image elements
    for (let i = 0; i < files.length; i++) {
        if (i >= 3) break;  // Stop after the first 3 images

        const file = files[i];
        if (file) {
            /**
             * The FileReader object used for reading files.
             * @type {FileReader}
             */
            const reader = new FileReader();
            reader.onload = (function(theImg) {
                return function(e) {
                    theImg.src = e.target.result;  // Update the src of the img element
                };
            })(document.getElementById('img-' + (i + 1)));  // Get the corresponding img element by id

            reader.readAsDataURL(file);  // Read the file as a Data URL
        }
    }
});
