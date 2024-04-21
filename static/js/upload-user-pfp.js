document.getElementById('upload-button').addEventListener('click', function() {
    document.getElementById('fileInput').click();  // Trigger the file input
});

document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];  // Get the first file selected by the user
    if (file) {
        const reader = new FileReader();  // Create a FileReader to read the file
        reader.onload = function(e) {
            const imgElement = document.getElementById('imageDisplay');
            uploadedimage.src = e.target.result;  // Update the src of the image element
        };
        reader.readAsDataURL(file);  // Read the file as a Data URL
    }
});