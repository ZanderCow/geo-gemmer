document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('gem-chart').getContext('2d');
    const data = gemVisitedFrequency;
    const monthOrder = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const sortedKeys = monthOrder.filter(month => Object.keys(data).includes(month));
    const chartLabels2 = sortedKeys;
    const chartData2 = sortedKeys.map(key => data[key]);

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

    const startColor2 = [77, 111, 63];
    const endColor2 = [163, 230, 134];
    const backgroundColors2 = interpolateColors(startColor2, endColor2, chartLabels2.length);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels2,
            datasets: [{
                label: 'Gem Visit Frequency',
                data: chartData2,
                backgroundColor: 'rgb(127,179,105)',
                borderColor: 'rgba(0,0,0,0.1)',
            }]
        },
        options: {
            maintainAspectRatio: true,
            legend: { display: false },
            scales: {
                xAxes: [{ ticks: { fontStyle: 'normal' } }],
                yAxes: [{ ticks: { beginAtZero: true, fontStyle: 'normal' } }]
            }
        }
    });



    



});
