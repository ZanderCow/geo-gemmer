
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('gemChart').getContext('2d');

    // Replace the static data with a Jinja2 variable
    // Assuming gem_variety_distribution is a dictionary like {'Restaurant': 2, 'Park': 1, ...}
    const data = {{ {{gem_distribution}} | tojson }};

    // Interpolate RGB colors from dark green to light green
    function interpolateColors(startColor, endColor, n) {
        const lerp = (start, end, t) => start + (end - start) * t;
        let colors = [];
        for (let i = 0; i < n; i++) {
            const t = i / (n - 1);
            const interpolatedColor = `rgb(${
                Math.round(lerp(startColor[0], endColor[0], t))
            },${
                Math.round(lerp(startColor[1], endColor[1], t))
            },${
                Math.round(lerp(startColor[2], endColor[2], t))
            })`;
            colors.push(interpolatedColor);
        }
        return colors;
    }

    const chartLabels = Object.keys(data);
    const chartData = Object.values(data);
    const startColor = [77, 111, 63]; // Dark green
    const endColor = [163, 230, 134]; // Light green
    const backgroundColors = interpolateColors(startColor, endColor, chartLabels.length); // Generate dynamic green colors

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Gem Variety',
                data: chartData,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(0,0,0,0.1)', // A consistent border color
            }]
        },
        options: {
            maintainAspectRatio: true,
            legend: {
                display: false,
                labels: {
                    fontStyle: 'normal'
                }
            },
            title: {
                display: true,
                text: 'Gem Details',
                fontStyle: 'bold'
            }
        }
    });
});

