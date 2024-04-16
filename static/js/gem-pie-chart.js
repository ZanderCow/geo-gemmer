document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('gem-pie-chart').getContext('2d');
    const data = gemDistribution;

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
    const startColor = [77, 111, 63];
    const endColor = [163, 230, 134];
    const backgroundColors = interpolateColors(startColor, endColor, chartLabels.length);

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Gem Variety',
                data: chartData,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(0,0,0,0.1)', // Consistent border color for visibility
            }]
        },
        options: {
            maintainAspectRatio: true,
            legend: {
                display: true, // Enable legend display
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