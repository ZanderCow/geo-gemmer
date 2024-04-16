document.addEventListener('DOMContentLoaded', function() {
    var slider = document.getElementById('distanceSlider');
    var output = document.getElementById('distanceValue');

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.innerHTML = this.value + " km";
    }
});