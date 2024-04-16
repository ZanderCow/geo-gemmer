

document.addEventListener("DOMContentLoaded", function() {
    // Listen for changes or clicks within any dropdown menu
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            const target = e.target;
            if (target.tagName === 'A' || target.tagName === 'INPUT') {
                updateDropdownText(target);
            }
        });
    });

    // Function to update the text of the dropdown button based on the selection
    function updateDropdownText(target) {
        const parentDropdown = target.closest('.dropdown');
        const dropdownId = parentDropdown.id;
        const dropdownButtonSpan = parentDropdown.querySelector('.btn.dropdown-toggle span');

        if (dropdownId === 'accessibility-dropdown' && target.type === 'checkbox') {
            // Handle checkbox selections for accessibility options
            updateAccessibilityText(parentDropdown, dropdownButtonSpan);
        } else if (target.type === 'range') {
            // Handle slider for distance
            dropdownButtonSpan.textContent = target.value + 'km';
        } else if (target.tagName === 'A') {
            // Handle selections from dropdown links
            dropdownButtonSpan.textContent = target.textContent.trim();
        }
    }

    // Function to compile and display selected accessibility options
    function updateAccessibilityText(dropdown, button) {
        let selectedOptions = [];
        dropdown.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            selectedOptions.push(checkbox.parentNode.textContent.trim());
        });
        button.textContent = selectedOptions.join(', ');
    }

    // Function to update the display of the distance as the slider is moved
    const distanceSlider = document.getElementById('distanceSlider');
    if (distanceSlider) {
        distanceSlider.oninput = function() {
            document.getElementById('distanceValue').textContent = this.value + 'km';
        };
    }
});
