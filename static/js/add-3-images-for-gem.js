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

//img2 swop with primary
document.getElementById('img-2').addEventListener('click', function() {
    img2 = document.getElementById('img-2');
    img1 = document.getElementById('img-1');
    var src = img2.src;

    img2.src = img1.src;
    img1.src = src;
});

//img3 swop with primary
document.getElementById('img-3').addEventListener('click', function() {
    img3 = document.getElementById('img-3');
    img1 = document.getElementById('img-1');
    var src = img3.src;

    img3.src = img1.src;
    img1.src = src;
});